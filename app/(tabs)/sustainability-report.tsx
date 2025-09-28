import { useRouter } from "expo-router";
import React from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { Avatar, Surface } from "react-native-paper";

const expiredThisMonth = 7; // Example value, replace with real calculation
const savedFromWaste = 12; // Example value, replace with real calculation
const barData = [
  { value: 3, label: "Apr" },
  { value: 5, label: "May" },
  { value: 2, label: "Jun" },
  { value: 7, label: "Jul" },
  { value: 4, label: "Aug" },
  { value: 6, label: "Sep" },
];

export default function SustainabilityReportScreen() {
  const router = useRouter();
  return (
    <View style={styles.container}>
      {/* Title and Profile Icon */}
      <View style={styles.headerRow}>
        <Text style={styles.heading}>Sustainability Report</Text>
        <TouchableOpacity onPress={() => router.push("/profile-settings")}>
          <Avatar.Icon size={40} icon="account" style={styles.avatar} />
        </TouchableOpacity>
      </View>

      {/* Expired Items Card */}
      <Surface style={styles.cardCircle} elevation={0}>
        <Text style={styles.cardCircleNumber}>{expiredThisMonth}</Text>
        <View style={{ alignItems: "center" }}>
          <Text style={styles.cardSubtitle}>expired items</Text>
          <Text style={styles.cardSubtitle}>this month</Text>
        </View>
      </Surface>

      {/* Bar Chart Card */}
      {/* <Surface style={styles.chartCard} elevation={0}>
        <Text style={styles.cardTitle}>Expired Items (Last 6 Months)</Text>
        <BarChart
          data={barData}
          barWidth={28}
          spacing={18}
          roundedTop
          frontColor="#b00020"
          yAxisThickness={0}
          xAxisColor="#e0e0e0"
          yAxisTextStyle={{ color: "#686666", fontSize: 12 }}
          xAxisLabelTextStyle={{ color: "#686666", fontSize: 12 }}
          noOfSections={4}
          maxValue={10}
          height={160}
          width={Dimensions.get("window").width - 48}
        />
      </Surface> */}

      <Surface style={styles.cardCircle} elevation={0}>
        <Text style={[styles.cardCircleNumber, { color: "#388e3c" }]}>
          {savedFromWaste}
        </Text>
        <View style={{ alignItems: "center" }}>
          <Text style={styles.cardSubtitle}>items saved</Text>
          <Text style={styles.cardSubtitle}>from food waste</Text>
        </View>
      </Surface>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
    paddingLeft: 16,
    paddingRight: 16,
    paddingTop: 8,
  },
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 24,
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
