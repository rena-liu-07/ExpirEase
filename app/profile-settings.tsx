import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Avatar } from "react-native-paper";

export default function SustainabilityReportScreen() {
  return (
    <View style={styles.container}>
      {/* Title and Profile Icon */}
      <View style={styles.headerRow}>
        <Text style={styles.heading}>Sustainability Report</Text>
        <Avatar.Icon size={40} icon="account" style={styles.avatar} />
      </View>

      {/* Expired Items Card */}
      {/* <Surface style={styles.cardCircle} elevation={0}>
        <Text style={styles.cardCircleNumber}>{expiredThisMonth}</Text>
        <View style={{ alignItems: "center" }}>
          <Text style={styles.cardSubtitle}>expired items</Text>
          <Text style={styles.cardSubtitle}>this month</Text>
        </View>
      </Surface>

      <Surface style={styles.cardCircle} elevation={0}>
        <Text style={[styles.cardCircleNumber, { color: "#388e3c" }]}>
          {savedFromWaste}
        </Text>
        <View style={{ alignItems: "center" }}>
          <Text style={styles.cardSubtitle}>items saved</Text>
          <Text style={styles.cardSubtitle}>from food waste</Text>
        </View>
      </Surface> */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
    padding: 16,
  },
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 24,
    marginTop: 8,
  },
  heading: {
    margin: 18,
    marginBottom: 18,
    fontSize: 20,
    fontWeight: 700,
    color: "#1a1a1a",
    textAlign: "center",
  },
  avatar: {
    backgroundColor: "#e7e7e7",
  },
  card: {
    borderRadius: 16,
    backgroundColor: "#fff",
    padding: 24,
    marginBottom: 24,
    alignItems: "center",
  },
  cardCircle: {
    height: 200,
    width: 200,
    borderRadius: 100,
    padding: 24,
    marginBottom: 24,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#e0e0e0",
    alignSelf: "center",
    justifyContent: "center",
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#686666",
    marginBottom: 6,
  },
  cardCircleNumber: {
    fontSize: 48,
    fontWeight: "bold",
    color: "#b00020",
    marginBottom: 2,
  },
  cardSubtitle: {
    fontSize: 16,
    color: "#686666",
  },
  chartCard: {
    borderRadius: 16,
    backgroundColor: "#fff",
    padding: 24,
    marginBottom: 24,
    alignItems: "center",
  },
});
