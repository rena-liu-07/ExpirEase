import Feather from "@expo/vector-icons/Feather";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, StyleSheet, TextInput, View } from "react-native";
import { Text } from "react-native-paper";
import { API_ENDPOINTS, apiCall } from "../../config/api";

export default function IndexSearchedScreen() {
  const [search, setSearch] = useState<string>("");
  const { query } = useLocalSearchParams();
  const [item, setItem] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (typeof query === "string") {
      setSearch(query);
      handleSearch(query);
    }
  }, [query]);

  const handleSearch = async (query?: string) => {
    const searchTerm = query ?? search;
    if (!searchTerm.trim()) return;
    setLoading(true);
    setError("");
    setItem(null);
    try {
      const data = await apiCall(
        `${API_ENDPOINTS.SEARCH}?q=${encodeURIComponent(searchTerm)}`
      );
      setItem(data);
    } catch (e) {
      setError("No ingredient found or network error.");
      setItem(null);
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Feather
          name="search"
          size={24}
          color="#828282"
          style={styles.searchIcon}
        />
        <TextInput
          placeholder="Search"
          underlineColorAndroid="transparent"
          style={styles.searchInput}
          value={search}
          onChangeText={setSearch}
          returnKeyType="search"
          onSubmitEditing={() => {
            handleSearch();
            setSearch("");
          }}
        />
      </View>
      <View style={styles.headingSection}>
        {loading && <ActivityIndicator />}
        {error ? <Text style={styles.error}>{error}</Text> : null}
        {item && (
          <>
            <Text style={styles.heading}>{item.name}</Text>
            <Text style={styles.subheading}>{item.category}</Text>
            <Text style={styles.expirationDate}>
              Expiration: {item.expiration}
            </Text>
          </>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
  },
  searchContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#e7e7e7",
    borderRadius: 8,
    margin: 18,
    marginBottom: 24,
    paddingLeft: 8,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    paddingTop: 8,
    paddingBottom: 8,
    paddingRight: 16,
    fontSize: 18,
    color: "#828282",
    backgroundColor: "transparent",
  },
  headingSection: {
    margin: 18,
  },
  heading: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#1a1a1a",
    marginBottom: 8,
  },
  subheading: {
    fontSize: 16,
    color: "#686666",
    marginBottom: 4,
  },
  expirationDate: {
    fontSize: 16,
    color: "#b00020",
  },
  error: {
    color: "#686666",
    fontSize: 20,
    marginTop: 10,
    textAlign: "center",
  },
});
