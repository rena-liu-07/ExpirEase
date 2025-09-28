import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { ScrollView, StyleSheet, TextInput, View } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import Swiper from "react-native-swiper";
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
            router.push({
              pathname: "/(tabs)/searched",
              params: { query: search },
            });
            setSearch("");
          }}
        />
      </View>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.headingSection}>
          <Text style={styles.heading}>Expiring Soon</Text>
          <Button
            mode="text"
            style={{ marginRight: 18 }}
            onPress={() => router.push("/index-see-all")}
            labelStyle={{ color: "#1a1a1a" }}
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
                  color="#eb5757"
                />
              </View>
            </View>
            <Swiper
              style={styles.swiperContainer}
              showsButtons={false}
              showsPagination={false}
              loop={false}
            >
              {group.items.map((item: any) => (
                <Card
                  key={item.name}
                  elevation={0}
                  style={styles.ingredientsCard}
                >
                  <Card.Content style={styles.cardTextContainer}>
                    <Text style={styles.cardCategory}>{item.category}</Text>
                    <Text style={styles.cardIngredient}>{item.name}</Text>
                  </Card.Content>
                </Card>
              ))}
            </Swiper>
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
    backgroundColor: "#e7e7e7",
    borderRadius: 8,
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
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a1a",
  },

  ingredientsSection: {
    margin: 18,
    marginTop: 0,
  },

  arrowCircle: {
    height: 20,
    width: 20,
    // backgroundColor: "#e7e7e7",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#eb5757",
  },

  ingredientsSectionTitle: {
    marginBottom: 12,
    fontSize: 16,
    fontWeight: 600,
    color: "#1a1a1a",
  },

  swiperContainer: {
    // gap: 10,
    height: 70,
  },

  ingredientsCard: {
    margin: 8,
    marginBottom: 18,
    marginRight: 16,
    borderRadius: 8,
    backgroundColor: "transparent",
    height: 61,
    width: 164,
    borderWidth: 1,
    borderColor: "#e0e0e0",
  },

  cardTextContainer: {
    paddingLeft: 10,
  },

  cardCategory: {
    fontSize: 12,
    color: "#686666",
  },

  cardIngredient: {
    paddingBottom: 2,
    fontSize: 14,
    color: "#1a1a1a",
  },
});
