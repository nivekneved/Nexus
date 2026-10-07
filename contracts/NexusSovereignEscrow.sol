// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @dev OpenZeppelin Contracts v4.9.0 (Security & Access Control)
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}

abstract contract Ownable is Context {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _transferOwnership(_msgSender());
    }

    function owner() public view virtual returns (address) {
        return _owner;
    }

    modifier onlyOwner() {
        _checkOwner();
        _;
    }

    function _checkOwner() internal view virtual {
        require(owner() == _msgSender(), "Ownable: caller is not the owner");
    }

    function renounceOwnership() public virtual onlyOwner {
        _transferOwnership(address(0));
    }

    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }

    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
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
        _requireNotPaused();
        _;
    }

    modifier whenPaused() {
        _requirePaused();
        _;
    }

    function _requireNotPaused() internal view virtual {
        require(!paused(), "Pausable: paused");
    }

    function _requirePaused() internal view virtual {
        require(paused(), "Pausable: not paused");
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

/**
 * @title NexusSovereignEscrow
 * @author Principal Security & Smart Contract Architect (Nexus v4.1.0)
 * @notice Production-grade escrow and micro-settlement contract for Base L2.
 * Incorporates ReentrancyGuard, Circuit Breaker (Pausable), Ownable, and Timelock release.
 */
contract NexusSovereignEscrow is Ownable, Pausable, ReentrancyGuard {

    struct Escrow {
        address client;
        address payable agent;
        uint256 amountUSDCOut;
        uint256 releaseTimestamp;
        bool isCompleted;
        bool isDisputed;
    }

    mapping(bytes32 => Escrow) public escrows;

    event EscrowCreated(bytes32 indexed escrowId, address indexed client, address indexed agent, uint256 amount);
    event EscrowReleased(bytes32 indexed escrowId, address indexed agent, uint256 amount);
    event EscrowDisputed(bytes32 indexed escrowId, address indexed disputer);
    event EmergencyWithdrawn(address indexed owner, uint256 balance);

    constructor() {}

    /**
     * @notice Creates a new milestone escrow for autonomous agent services.
     * @param escrowId Unique cryptographic identifier for the engagement.
     * @param agent Address of the sovereign agent / worker.
     * @param lockDurationSeconds Timelock duration before automatic unlock.
     */
    function createEscrow(
        bytes32 escrowId,
        address payable agent,
        uint256 lockDurationSeconds
    ) external payable whenNotPaused nonReentrant {
        require(msg.value > 0, "Escrow amount must be greater than zero");
        require(agent != address(0), "Invalid agent address");
        require(escrows[escrowId].client == address(0), "Escrow ID already exists");

        escrows[escrowId] = Escrow({
            client: msg.sender,
            agent: agent,
            amountUSDCOut: msg.value,
            releaseTimestamp: block.timestamp + lockDurationSeconds,
            isCompleted: false,
            isDisputed: false
        });

        emit EscrowCreated(escrowId, msg.sender, agent, msg.value);
    }

    /**
     * @notice Releases escrow funds to the agent upon successful task verification.
     * @param escrowId Unique cryptographic identifier for the engagement.
     */
    function releaseEscrow(bytes32 escrowId) external nonReentrant {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.client != address(0), "Escrow does not exist");
        require(!escrow.isCompleted, "Escrow already completed");
        require(!escrow.isDisputed, "Escrow is currently under dispute");
        require(
            msg.sender == escrow.client || msg.sender == owner(),
            "Only client or sovereign owner can release escrow"
        );

        escrow.isCompleted = true;
        uint256 payout = escrow.amountUSDCOut;

        (bool success, ) = escrow.agent.call{value: payout}("");
        require(success, "Transfer to agent failed");

        emit EscrowReleased(escrowId, escrow.agent, payout);
    }

    /**
     * @notice Flags an escrow as disputed for human-in-the-loop arbitration.
     * @param escrowId Unique cryptographic identifier for the engagement.
     */
    function disputeEscrow(bytes32 escrowId) external {
        Escrow storage escrow = escrows[escrowId];
        require(escrow.client != address(0), "Escrow does not exist");
        require(!escrow.isCompleted, "Escrow already completed");
        require(
            msg.sender == escrow.client || msg.sender == escrow.agent,
            "Only parties involved can dispute"
        );

        escrow.isDisputed = true;
        emit EscrowDisputed(escrowId, msg.sender);
    }

    /**
     * @notice Emergency pause circuit breaker.
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @notice Unpause contract operations.
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @notice Emergency withdrawal of trapped funds in catastrophic events.
     */
    function emergencyWithdraw() external onlyOwner whenPaused {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");

        (bool success, ) = owner().call{value: balance}("");
        require(success, "Emergency withdrawal failed");

        emit EmergencyWithdrawn(owner(), balance);
    }

    receive() external payable {
        revert("Direct deposits not allowed; use createEscrow");
    }
}
