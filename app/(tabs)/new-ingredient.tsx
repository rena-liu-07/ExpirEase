import * as ImagePicker from "expo-image-picker";
import React, { useRef, useState } from "react";
import {
  Alert,
  Animated,
  Easing,
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

export default function NewIngredientScreen() {
  const [mode, setMode] = useState("manual");
  const anim = useRef(new Animated.Value(0)).current;
  const [photos, setPhotos] = useState<string[]>([]);
  const [webFiles, setWebFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Form state variables
  const [ingredientName, setIngredientName] = useState("");
  const [category, setCategory] = useState("");
  const [expirationDate, setExpirationDate] = useState("");
  const [userId] = useState("1"); // Mock user ID

  // Permission for media library
  const requestMediaLibraryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== "granted") {
      Alert.alert(
        "Media library permission denied",
        "Please enable photo library access in settings."
      );
      return false;
    }
    return true;
  };

  // Pick images from device library
  const pickImages = async () => {
    if (Platform.OS === "web") {
      // For web, use file input
      if (fileInputRef.current) {
        fileInputRef.current.click();
      }
    } else {
      // For mobile, use ImagePicker
      const hasPermission = await requestMediaLibraryPermission();
      if (!hasPermission) return;
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: "images",
        allowsMultipleSelection: true,
        selectionLimit: 20,
        quality: 1,
      });
      if (!result.canceled && result.assets?.length) {
        const newPhotos = [
          ...photos,
          ...result.assets.map((asset) => asset.uri),
        ];
        setPhotos(newPhotos);
        handlePhotoSubmission(newPhotos);
      }
    }
  };

  // Handle web file selection
  const handleWebFileSelect = (event: any) => {
    const files = Array.from(event.target.files) as File[];
    if (files.length > 0) {
      setWebFiles([...webFiles, ...files]);
      const newPhotos = [
        ...photos,
        ...files.map((file) => URL.createObjectURL(file)),
      ];
      setPhotos(newPhotos);
      handlePhotoSubmission(undefined, files);
    }
  };

  // Remove photo
  const removePhoto = (uri: string) => {
    setPhotos(photos.filter((photo) => photo !== uri));
  };

  const handlePhotoSubmission = async (photoArray = photos, files?: File[]) => {
    try {
      console.log("handlePhotoSubmission called");
      console.log("Platform.OS:", Platform.OS);
      console.log("files:", files);
      console.log("webFiles.length:", webFiles.length);
      console.log("photos.length:", photoArray.length);

      if (Platform.OS === "web" && files && files.length > 0) {
        // For web, use actual File objects
        const formData = new FormData();
        files.forEach((file) => {
          formData.append("images", file);
        });
        const response = await fetch("http://localhost:5000/photo_scanner", {
          method: "POST",
          body: formData as any,
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Scanner response:", data);
        Alert.alert("Success", "Photo processed successfully!");
      } else if (Platform.OS === "web" && webFiles.length > 0) {
        // Use stored web files
        const formData = new FormData();
        webFiles.forEach((file) => {
          formData.append("images", file);
        });
        const response = await fetch("http://localhost:5000/photo_scanner", {
          method: "POST",
          body: formData as any,
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Scanner response:", data);
        Alert.alert("Success", "Photo processed successfully!");
      } else {
        Alert.alert("Error", "No images to upload");
      }
    } catch (error) {
      console.error("Error:", error);
      Alert.alert("Error", String((error as any)?.message || error));
    }
  };

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
      const response = await fetch("http://192.168.1.100:8080/add_ingredient", {
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
            style={[
              styles.toggleText,
              mode === "manual" && styles.toggleTextActive,
            ]}
          >
            Manual
          </Text>
          <Text
            style={[
              styles.toggleText,
              mode === "photo" && styles.toggleTextActive,
            ]}
          >
            Photo
          </Text>
        </View>
      </TouchableOpacity>
      {mode === "manual" ? (
        <View style={styles.manualSection}>
          <TextInput style={styles.input} placeholder="Ingredient Name" />
          <TextInput style={styles.input} placeholder="Category" />
          <TextInput
            style={styles.input}
            placeholder="Expiration Date (YYYY-MM-DD)"
          />
          <TouchableOpacity style={styles.buttonContainer}>
            <Text style={styles.buttonText}>Add Ingredient</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.photoTabRectangle}>
          {Platform.OS === "web" && (
            <input
              ref={fileInputRef as any}
              type="file"
              accept="image/*"
              multiple
              style={{ display: "none" }}
              onChange={handleWebFileSelect}
            />
          )}
          <TouchableOpacity style={styles.selectButton} onPress={pickImages}>
            <Text style={styles.selectButtonText}>
              Select Photos from Device
            </Text>
          </TouchableOpacity>
          <View style={styles.photoDisplayAreaGrid}>
            {photos.length > 0 ? (
              <ScrollView contentContainerStyle={styles.photoGridScrollContent}>
                <View style={styles.photoGrid}>
                  {photos.map((uri) => (
                    <View key={uri} style={styles.imageContainerDisplay}>
                      <Image source={{ uri }} style={styles.imageDisplay} />
                      <TouchableOpacity
                        style={styles.deleteButton}
                        onPress={() => removePhoto(uri)}
                      >
                        <Text style={styles.deleteButtonText}>Delete</Text>
                      </TouchableOpacity>
                    </View>
                  ))}
                </View>
              </ScrollView>
            ) : (
              <Text style={styles.photoPlaceholder}>No photos yet</Text>
            )}
          </View>
          <TouchableOpacity
            style={styles.scanButton}
            onPress={() => handlePhotoSubmission()}
          >
            <Text style={styles.scanButtonText}>Scan</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

const TOGGLE_WIDTH = 157;
const TOGGLE_HEIGHT = 32;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fcfcfa", padding: 24 },
  heading: {
    margin: 18,
    marginBottom: 18,
    fontSize: 20,
    fontWeight: "700",
    color: "#1a1a1a",
    textAlign: "center",
  },
  toggleContainer: {
    width: TOGGLE_WIDTH,
    height: TOGGLE_HEIGHT,
    borderRadius: TOGGLE_HEIGHT / 2,
    backgroundColor: "#e7e7e7",
    marginBottom: 24,
    overflow: "hidden",
    alignSelf: "center",
    justifyContent: "center",
  },
  toggleBackground: {
    position: "absolute",
    width: TOGGLE_WIDTH / 2,
    height: TOGGLE_HEIGHT,
    backgroundColor: "#eb5757",
    borderRadius: TOGGLE_HEIGHT / 2,
    zIndex: 1,
  },
  toggleContent: {
    flexDirection: "row",
    width: TOGGLE_WIDTH,
    height: TOGGLE_HEIGHT,
    alignItems: "center",
    justifyContent: "space-between",
    zIndex: 2,
  },
  toggleText: {
    flex: 1,
    textAlign: "center",
    color: "#686666",
    fontSize: 14,
    fontWeight: "500",
  },
  toggleTextActive: { color: "#fff" },
  manualSection: { marginTop: 16 },
  input: {
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "#e0e0e0",
    color: "#828282",
  },
  buttonContainer: {
    backgroundColor: "#eb5757",
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    color: "#fcfcfa",
    fontSize: 16,
  },
  photoTabRectangle: {
    width: "100%",
    minHeight: 350,
    maxHeight: "80%",
    backgroundColor: "#fcfcfa",
    borderRadius: 8,
    padding: 12,
    marginTop: 16,
    alignItems: "center",
    justifyContent: "flex-start",
    flexGrow: 1,
  },
  selectButton: {
    backgroundColor: "transparent",
    borderRadius: 8,
    paddingVertical: 8,
    paddingHorizontal: 18,
    marginBottom: 16,
    alignSelf: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#686666",
    // Remove alignSelf: "stretch" and make width fit content
  },
  selectButtonText: {
    color: "#1a1a1a",
    fontSize: 16,
    fontWeight: "600",
  },
  photoDisplayAreaGrid: {
    flex: 1,
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 8,
    minHeight: 0,
  },
  photoGridScrollContent: {
    alignItems: "center",
    paddingVertical: 8,
    flexGrow: 1,
  },
  photoGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "flex-start",
    alignItems: "flex-start",
    width: "100%",
  },
  imageContainerDisplay: {
    marginRight: 16,
    marginBottom: 16,
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  imageDisplay: {
    width: 120,
    height: 120,
    borderRadius: 8,
    marginBottom: 8,
  },
  deleteButton: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "#e0e0e0",
    borderRadius: 6,
    paddingVertical: 6,
    paddingHorizontal: 16,
    marginTop: 4,
  },
  deleteButtonText: {
    color: "#1a1a1a",
    fontWeight: "600",
    fontSize: 14,
  },
  photoPlaceholder: {
    color: "#686666",
    fontSize: 16,
    marginTop: 24,
  },
  scanButton: {
    backgroundColor: "#eb5757",
    borderWidth: 1,
    borderColor: "#e0e0e0",
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 32,
    marginTop: 18,
    alignSelf: "center",
    alignItems: "center",
  },
  scanButtonText: {
    color: "#fcfcfa",
    fontSize: 18,
    fontWeight: "600",
    letterSpacing: 1,
  },
});
