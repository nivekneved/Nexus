import React from "react";
import { SafeAreaView, Text, View, StyleSheet } from "react-native";

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>ReceiptChase - Nexus Turnkey Asset</Text>
      </View>
      <Text style={styles.pitch}>Idiot-proof receipt catcher for blue-collar teams.</Text>
      <Text style={styles.status}>Status: Scaffolding Complete. Awaiting JIT Module Injection.</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#111", justifyContent: "center", alignItems: "center", padding: 20 },
  header: { marginBottom: 20 },
  title: { fontSize: 24, fontWeight: "bold", color: "#fff" },
  pitch: { fontSize: 16, color: "#aaa", textAlign: "center", marginBottom: 10 },
  status: { fontSize: 14, color: "#4ade80", marginTop: 20 }
});
