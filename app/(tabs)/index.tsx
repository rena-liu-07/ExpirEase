import Slider from "@/components/Slider";
import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { ScrollView, StyleSheet, TextInput, View } from "react-native";
import { Button, Text } from "react-native-paper";
import { API_ENDPOINTS, apiCall } from "../../config/api";

const EXPIRY_GROUPS = [
  { label: "Expiring Today", test: (days: number) => days === 0 },
  { label: "Expiring Tomorrow", test: (days: number) => days === 1 },
  { label: "Expiring In 2 Days", test: (days: number) => days === 2 },
  { label: "Expiring In 3 Days", test: (days: number) => days === 3 },
  {
    label: "Expiring In <1 Week",
    test: (days: number) => days > 3 && days < 7,
  },
  {
    label: "Expiring In <1 Month",
    test: (days: number) => days >= 7 && days < 30,
  },
];

function groupIngredients(ingredients: any[]) {
  const today = new Date();
  const used = new Set();
  const groups = EXPIRY_GROUPS.map((g) => ({ ...g, items: [] as any[] }));

  for (const ing of ingredients) {
    const exp = new Date(ing.expiration);
    const days = Math.floor(
      (exp.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
    );
    for (const group of groups) {
      if (group.test(days) && !used.has(ing.name)) {
        group.items.push(ing);
        used.add(ing.name);
        break;
      }
    }
  }
  return groups.filter((g) => g.items.length > 0);
}

export default function Index() {
  const router = useRouter();
  const [search, setSearch] = useState("");
  const [groups, setGroups] = useState<any[]>([]);

  useEffect(() => {
    apiCall(API_ENDPOINTS.ALL_INGREDIENTS)
      .then((data) => setGroups(groupIngredients(data as any[])))
      .catch((error) => console.error("Failed to load ingredients:", error));
  }, []);

  return (
    <View style={[styles.container, { flex: 1, minHeight: 0 }]}>
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
            router.push({
              pathname: "/(tabs)/searched",
              params: { query: search },
            });
            setSearch("");
          }}
        />
      </View>
      <ScrollView
        showsVerticalScrollIndicator={false}
        style={{ flex: 1 }}
        contentContainerStyle={{ flexGrow: 1 }}
      >
        <View style={styles.headingSection}>
          <Text style={styles.heading}>Expiring Soon</Text>
          <Button
            mode="text"
            style={{ marginRight: 18 }}
            onPress={() => router.push("/index-see-all")}
            labelStyle={{ color: "#eb5757" }}
          >
            See All
          </Button>
        </View>
        {groups.map((group) => (
          <View key={group.label} style={styles.ingredientsSection}>
            <View style={{ flexDirection: "row", gap: 10 }}>
              <Text style={styles.ingredientsSectionTitle}>{group.label}</Text>
              <View
                style={[
                  groups.length > 2 ? { display: "flex" } : { display: "none" }, // not working ?
                  styles.arrowCircle,
                ]}
              >
                <MaterialIcons
                  name="arrow-forward-ios"
                  size={13}
                  color="#1a1a1a"
                />
              </View>
            </View>
            <Slider data={group.items} />
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
  },

  searchContainer: {
    margin: 18,
    marginBottom: 24,
    paddingLeft: 8,
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#fffffe",
    borderRadius: 8,
    borderWidth: 2,
    borderColor: "#e7e7e7",
    // shadowColor: "#686666",
    // shadowOpacity: 1,
    // shadowRadius: 3,
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
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  heading: {
    margin: 18,
    marginTop: 8,
    marginBottom: 4,
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a1a",
  },

  ingredientsSection: {
    margin: 18,
    marginTop: 16,
  },

  arrowCircle: {
    height: 20,
    width: 20,
    backgroundColor: "#e7e7e7",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
    // borderWidth: 1,
    // borderColor: "#eb5757",
  },

  ingredientsSectionTitle: {
    marginBottom: 8,
    fontSize: 16,
    fontWeight: 600,
    color: "#eb5757",
  },
});
