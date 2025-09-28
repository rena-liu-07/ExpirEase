import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useRouter } from "expo-router";
import React from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { Avatar, Button } from "react-native-paper";

export default function SustainabilityReportScreen() {
  const router = useRouter();
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => router.replace("/(tabs)/sustainability-report")}
          style={styles.iconButton}
        >
          <MaterialIcons name="arrow-back-ios" size={22} color="black" />
        </TouchableOpacity>
        <Text style={styles.heading}>Profile Settings</Text>
        <Avatar.Icon size={40} icon="account" style={styles.avatar} />
      </View>

      <View>
        <Text>Username: </Text>
        <Text>Email: </Text>
        <Text>Password: </Text>
        <Button>Log Out</Button>
        <Button>Delete Account</Button>
      </View>
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
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 24,
  },
  iconButton: {
    padding: 8,
    paddingLeft: 4,
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
