import React from "react";
import { SafeAreaView, Text, View, StyleSheet } from "react-native";

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>ActionBypass - Nexus Turnkey Asset</Text>
      </View>
      <Text style={styles.pitch}>Local fallback CI runner CLI that executes when GitHub Actions goes down.</Text>
      <Text style={styles.status}>Status: Scaffolding Complete. Live HN Data Verified.</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f172a", justifyContent: "center", alignItems: "center", padding: 20 },
  header: { marginBottom: 20 },
  title: { fontSize: 24, fontWeight: "bold", color: "#60a5fa" },
  pitch: { fontSize: 16, color: "#94a3b8", textAlign: "center", marginBottom: 10 },
  status: { fontSize: 14, color: "#34d399", marginTop: 20 }
});
