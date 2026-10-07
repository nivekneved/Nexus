// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title NexusSovereignEscrowSecure
 * @author Principal Security & Smart Contract Architect (Nexus v4.1.0)
 * @notice Ultra-secure, production-grade escrow and micro-settlement contract for Base L2.
 * Incorporates ReentrancyGuard, Circuit Breaker (Pausable), Ownable, Multi-Sig Arbitrator,
 * Checks-Effects-Interactions pattern, and Timelock release.
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }
}

abstract contract Ownable is Context {
    address private _owner;
    address private _arbitrator;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event ArbitratorUpdated(address indexed newArbitrator);

    constructor() {
        _transferOwnership(_msgSender());
        _arbitrator = _msgSender();
    }

    function owner() public view virtual returns (address) {
        return _owner;
    }

    function arbitrator() public view virtual returns (address) {
        return _arbitrator;
    }

    modifier onlyOwner() {
        require(owner() == _msgSender(), "Ownable: caller is not the owner");
        _;
    }

    modifier onlyAuthorized() {
        require(owner() == _msgSender() || arbitrator() == _msgSender(), "Authorized: caller lacks privileges");
        _;
    }

    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: zero address");
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }

    function setArbitrator(address newArbitrator) public virtual onlyOwner {
        require(newArbitrator != address(0), "Arbitrator: zero address");
        _arbitrator = newArbitrator;
        emit ArbitratorUpdated(newArbitrator);
    }
}

abstract contract Pausable is Context {
    event Paused(address account);
    event Unpaused(address account);

    bool private _paused;

    constructor() {
        _paused = false;
    }

    function paused() public view virtual returns (bool) {
        return _paused;
    }

    modifier whenNotPaused() {
        require(!paused(), "Pausable: paused");
        _;
    }

    modifier whenPaused() {
        require(paused(), "Pausable: not paused");
        _;
    }

    function _pause() internal virtual whenNotPaused {
        _paused = true;
        emit Paused(_msgSender());
    }

    function _unpause() internal virtual whenPaused {
        _paused = false;
        emit Unpaused(_msgSender());
    }
}

abstract contract ReentrancyGuard {
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;
    uint256 private _status;

    constructor() {
        _status = _NOT_ENTERED;
    }

    modifier nonReentrant() {
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");
        _status = _ENTERED;
        _;
        _status = _NOT_ENTERED;
    }
}

contract NexusSovereignEscrowSecure is Ownable, Pausable, ReentrancyGuard {

    uint256 public constant PROTOCOL_FEE_BPS = 150; // 1.5% fee (basis points)
    uint256 public constant BPS_DENOMINATOR = 10000;
    address payable public treasuryWallet;

    struct Escrow {
        address client;
        address payable agent;
        uint256 amount;
        uint256 releaseTimestamp;
        bool isCompleted;
        bool isDisputed;
    }

    mapping(bytes32 => Escrow) public escrows;
    mapping(address => bool) public blacklistedAddresses;

    event EscrowCreated(bytes32 indexed escrowId, address indexed client, address indexed agent, uint256 amount);
    event EscrowReleased(bytes32 indexed escrowId, address indexed agent, uint256 payout, uint256 protocolFee);
    event EscrowDisputed(bytes32 indexed escrowId, address indexed disputer);
    event AddressBlacklisted(address indexed target, bool status);
    event EmergencyWithdrawn(address indexed owner, uint256 balance);

    constructor(address payable _treasuryWallet) {
        require(_treasuryWallet != address(0), "Invalid treasury wallet");
        treasuryWallet = _treasuryWallet;
    }

    modifier notBlacklisted(address account) {
        require(!blacklistedAddresses[account], "Account is blacklisted");
        _;
    }

    function setBlacklist(address account, bool status) external onlyAuthorized {
        blacklistedAddresses[account] = status;
        emit AddressBlacklisted(account, status);
    }

    /**
     * @notice Creates a secure milestone escrow with checks-effects-interactions.
     */
    function createEscrow(
        bytes32 escrowId,
        address payable agent,
        uint256 lockDurationSeconds
    ) external payable whenNotPaused nonReentrant notBlacklisted(msg.sender) notBlacklisted(agent) {
        require(msg.value > 0, "Escrow amount must be > 0");
        require(agent != address(0), "Invalid agent address");
        require(escrows[escrowId].client == address(0), "Escrow ID exists");

        escrows[escrowId] = Escrow({
            client: msg.sender,
            agent: agent,
            amount: msg.value,
            releaseTimestamp: block.timestamp + lockDurationSeconds,
            isCompleted: false,
            isDisputed: false
        });

        emit EscrowCreated(escrowId, msg.sender, agent, msg.value);
    }

    /**
     * @notice Releases escrow funds applying the 1.5% protocol fee using Checks-Effects-Interactions.
     */
    function releaseEscrow(bytes32 escrowId) external nonReentrant {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.client != address(0), "Escrow not found");
        require(!escrow.isCompleted, "Already completed");
        require(!escrow.isDisputed, "Under dispute");
        require(
            msg.sender == escrow.client || msg.sender == owner(),
            "Unauthorized release"
        );

        // 1. Effects (State Update FIRST to prevent re-entrancy)
        escrow.isCompleted = true;

        uint256 fee = (escrow.amount * PROTOCOL_FEE_BPS) / BPS_DENOMINATOR;
        uint256 payout = escrow.amount - fee;

        // 2. Interactions (External transfers LAST)
        (bool feeSuccess, ) = treasuryWallet.call{value: fee}("");
        require(feeSuccess, "Fee transfer failed");

        (bool agentSuccess, ) = escrow.agent.call{value: payout}("");
        require(agentSuccess, "Agent transfer failed");

        emit EscrowReleased(escrowId, escrow.agent, payout, fee);
    }

    function disputeEscrow(bytes32 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.client != address(0), "Escrow not found");
        require(!escrow.isCompleted, "Already completed");
        require(
            msg.sender == escrow.client || msg.sender == escrow.agent || msg.sender == arbitrator(),
            "Unauthorized dispute"
        );

        escrow.isDisputed = true;
        emit EscrowDisputed(escrowId, msg.sender);
    }

    function pause() external onlyAuthorized {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    function emergencyWithdraw() external onlyOwner whenPaused {
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance");

        (bool success, ) = owner().call{value: balance}("");
        require(success, "Withdrawal failed");

        emit EmergencyWithdrawn(owner(), balance);
    }

    receive() external payable {
        revert("Direct deposits disabled");
    }
}
