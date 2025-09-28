import React, { useRef, useState } from "react";
import {
  Alert,
  Animated,
  Easing,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

export default function NewIngredientScreen() {
  const [mode, setMode] = useState("manual");
  const anim = useRef(new Animated.Value(0)).current;
  const [ingredientName, setIngredientName] = useState("");
  const [category, setCategory] = useState("");
  const [expirationDate, setExpirationDate] = useState("");
  const userId = 1; // 测试用，正式环境可替换成登录获取的 user_id

  const toggle = () => {
    const next = mode === "manual" ? "photo" : "manual";
    setMode(next);
    Animated.timing(anim, {
      toValue: next === "manual" ? 0 : 1,
      duration: 250,
      easing: Easing.inOut(Easing.ease),
      useNativeDriver: false,
    }).start();
  };

  const translateX = anim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 78.5],
  });

  const handleAddIngredient = async () => {
    if (!ingredientName || !category || !expirationDate) {
      Alert.alert("Error", "Please fill in all fields.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8080/add_ingredient", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          name: ingredientName,
          category,
          expiration_date: expirationDate,
        }),
      });

      const data = await response.json();
      if (response.ok && data.success) {
        Alert.alert("Success", "Ingredient added!");
        setIngredientName("");
        setCategory("");
        setExpirationDate("");
      } else {
        Alert.alert("Error", data.error || "Failed to add ingredient.");
      }
    } catch (error) {
      Alert.alert("Error", "Failed to connect to server.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Add New Ingredient</Text>

      <TouchableOpacity
        style={styles.toggleContainer}
        onPress={toggle}
        activeOpacity={0.8}
      >
        <Animated.View
          style={[styles.toggleBackground, { transform: [{ translateX }] }]}
        />
        <View style={styles.toggleContent}>
          <Text
            style={[styles.toggleText, mode === "manual" && styles.toggleTextActive]}
          >
            Manual
          </Text>
          <Text
            style={[styles.toggleText, mode === "photo" && styles.toggleTextActive]}
          >
            Photo
          </Text>
        </View>
      </TouchableOpacity>

      {mode === "manual" ? (
        <View style={styles.manualSection}>
          <TextInput
            style={styles.input}
            placeholder="Ingredient Name"
            value={ingredientName}
            onChangeText={setIngredientName}
          />
          <TextInput
            style={styles.input}
            placeholder="Category"
            value={category}
            onChangeText={setCategory}
          />
          <TextInput
            style={styles.input}
            placeholder="Expiration Date (YYYY-MM-DD)"
            value={expirationDate}
            onChangeText={setExpirationDate}
          />
          <TouchableOpacity
            style={styles.buttonContainer}
            onPress={handleAddIngredient}
          >
            <Text style={styles.buttonText}>Add Ingredient</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.photoSection}>
          <Text style={styles.photoPlaceholder}>[Photo input section here]</Text>
        </View>
      )}
    </View>
  );
}

const TOGGLE_WIDTH = 157;
const TOGGLE_HEIGHT = 32;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fcfcfa", padding: 24 },
  heading: { margin: 18, marginBottom: 18, fontSize: 20, fontWeight: "700", color: "#1a1a1a", textAlign: "center" },
  toggleContainer: { width: TOGGLE_WIDTH, height: TOGGLE_HEIGHT, borderRadius: TOGGLE_HEIGHT / 2, backgroundColor: "#e7e7e7", marginBottom: 24, overflow: "hidden", alignSelf: "center", justifyContent: "center" },
  toggleBackground: { position: "absolute", width: TOGGLE_WIDTH / 2, height: TOGGLE_HEIGHT, backgroundColor: "#1a1a1a", borderRadius: TOGGLE_HEIGHT / 2, zIndex: 1 },
  toggleContent: { flexDirection: "row", width: TOGGLE_WIDTH, height: TOGGLE_HEIGHT, alignItems: "center", justifyContent: "space-between", zIndex: 2 },
  toggleText: { flex: 1, textAlign: "center", color: "#686666", fontSize: 14, fontWeight: "500" },
  toggleTextActive: { color: "#fff" },
  manualSection: { marginTop: 16 },
  input: { backgroundColor: "#fff", borderRadius: 8, padding: 12, fontSize: 16, marginBottom: 16, borderWidth: 1, borderColor: "#e0e0e0", color: "#828282" },
  buttonContainer: { backgroundColor: "#1a1a1a", borderRadius: 8, padding: 12, marginBottom: 16, borderWidth: 1, justifyContent: "center", alignItems: "center" },
  buttonText: { color: "#fcfcfa", fontSize: 16 },
  photoSection: { marginTop: 16, alignItems: "center", justifyContent: "center", height: 150, backgroundColor: "#f3e5f5", borderRadius: 8 },
  photoPlaceholder: { color: "#686666", fontSize: 16 },
});
