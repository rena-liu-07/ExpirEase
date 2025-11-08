// Import the Expo ImagePicker API for accessing camera and photo library
import * as ImagePicker from 'expo-image-picker';
// Import React and useState hook
import * as React from 'react';
import { useState } from 'react';
// Import UI components and utilities from React Native
import { Alert, Button, Image, ScrollView, StyleSheet, View } from 'react-native';
// Import API configuration
import { API_ENDPOINTS } from './config/api';

// Main component definition
export default function PhotoUploader() {
  // State to store photo URIs
  const [photos, setPhotos] = useState<string[]>([]);

  // Request permission to use the camera
  const requestCameraPermission = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Camera permission denied', 'Please enable camera access in settings.');
      return false;
    }
    return true;
  };

  // Request permission to access the media library
  const requestMediaLibraryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Media library permission denied', 'Please enable photo library access in settings.');
      return false;
    }
    return true;
  };

  // Function to take a photo using the device camera
  const takePhoto = async () => {
    const hasPermission = await requestCameraPermission();
    if (!hasPermission) return;

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images, // Only allow images
      quality: 1, // Highest quality
    });

    // If photo was taken successfully, add it to the state
    if (!result.canceled && result.assets?.length) {
      setPhotos([...photos, result.assets[0].uri]);
    }

    sendToFlask();
  };

  // Function to pick images from the photo library
  const pickImage = async () => {
    const hasPermission = await requestMediaLibraryPermission();
    if (!hasPermission) return;

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images, // Only allow images
      allowsMultipleSelection: true, // Enable selecting multiple images
      selectionLimit: 10, // Limit to 10 images
      quality: 1, // Highest quality
    });

    // If images were selected, add them to the state
    if (!result.canceled && result.assets?.length) {
      setPhotos([...photos, ...result.assets.map(asset => asset.uri)]);
    }
  };

  // Function to remove a photo from the state
  const removePhoto = (uri: string) => {
    setPhotos(photos.filter(photo => photo !== uri));
  };

  const sendToFlask = async () => {
    try {
      if (photos.length === 0) {
        Alert.alert('Error', 'No photo to upload');
        return;
      }
      const photoUri = photos[0]; // Only send the first photo for now
      const formData = new FormData();
      formData.append('image', {
        uri: photoUri,
        type: 'image/jpeg',
        name: photoUri.split('/').pop() || 'photo.jpg',
      } as any); // React Native FormData workaround

      console.log('Sending photo to:', API_ENDPOINTS.PHOTO_SCANNER);
      const response = await fetch(API_ENDPOINTS.PHOTO_SCANNER, {
        method: 'POST',
        body: formData,
        // Do NOT set Content-Type header!
      });
      
      if (!response.ok) {
        const text = await response.text();
        throw new Error('Network response was not ok: ' + text);
      }
      
      const data = await response.json();
      console.log('Response from server:', data);
      
      if (data.success && data.results && data.results.length > 0) {
        const items = data.results[0]; // Get first image results
        const itemNames = items.map((item: any) => item.item).join(', ');
        Alert.alert(
          '✅ Scan Complete!', 
          `Found ${items.length} items: ${itemNames}\n\nThese have been added to your expiring food list.`,
          [{ text: 'OK', onPress: () => setPhotos([]) }] // Clear photos after success
        );
      } else {
        Alert.alert('Scan Complete', 'No items found in the image.');
      }
    } catch (error) {
      console.error('Error sending photo:', error);
      Alert.alert('Error', String((error as any)?.message || error));
    }
  };

  // Render the UI
  return (
    <View style={styles.container}>
      {/* Button to take a photo */}
      <Button title="Take Photo" onPress={takePhoto} />
      {/* Button to upload photos from library */}
      <Button title="Upload Photos" onPress={pickImage} />
      {/* Horizontal scroll view to display selected photos */}
      <ScrollView horizontal>
        {photos.map(uri => (
          <View key={uri} style={styles.imageContainer}>
            {/* Display the image */}
            <Image source={{ uri }} style={styles.image} />
            {/* Button to delete the image */}
            <Button title="Delete" onPress={() => removePhoto(uri)} />
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

// Styling for the component
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  imageContainer: {
    margin: 10,
    alignItems: 'center',
  },
  image: {
    width: 120,
    height: 120,
    borderRadius: 10,
  },
});