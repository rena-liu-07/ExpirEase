import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import {
  Dimensions,
  FlatList,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  View,
} from "react-native";
import { Swipeable } from "react-native-gesture-handler";
import { Card, Text } from "react-native-paper";
import { API_ENDPOINTS, apiCall } from "../config/api";

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
  if (!Array.isArray(ingredients)) {
    console.warn("groupIngredients: ingredients is not an array:", ingredients);
    return [];
  }

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

export default function IndexSeeAllScreen() {
  const router = useRouter();
  const [groups, setGroups] = useState<any[]>([]);

  const handleDelete = async (name: string) => {
    try {
      await apiCall(
        `${API_ENDPOINTS.DELETE_INGREDIENT}?name=${encodeURIComponent(name)}`,
        {
          method: "DELETE",
        }
      );
      setGroups((prev: any[]) =>
        prev.filter((item: any) => item.name !== name)
      );
    } catch (error) {
      console.error("Failed to delete ingredient:", error);
    }
  };

  const renderItem = ({ item }: { item: any }) => (
    <Swipeable
      renderRightActions={() => (
        <View style={styles.deleteSlide}>
          <Feather name="trash-2" size={24} color="white" />
        </View>
      )}
      onSwipeableOpen={() => handleDelete(item.name)}
    >
      <Card style={styles.ingredientsCard} elevation={0}>
        <Card.Content style={styles.cardTextContainer}>
          <Text style={styles.cardCategory}>{item.category}</Text>
          <Text style={styles.cardIngredient}>{item.name}</Text>
        </Card.Content>
      </Card>
    </Swipeable>
  );

  useEffect(() => {
    const loadIngredients = async () => {
      try {
        const data = await apiCall(API_ENDPOINTS.ALL_INGREDIENTS);
        // Ensure data is an array before processing
        const ingredientsArray = Array.isArray(data) ? data : [];
        setGroups(groupIngredients(ingredientsArray));
      } catch (error) {
        console.error("Failed to load ingredients:", error);
        setGroups([]);
      }
    };

    loadIngredients();
  }, []);

  return (
    <View style={{ backgroundColor: "#fcfcfa" }}>
      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => router.replace("/(tabs)")}
          style={styles.iconButton}
        >
          <MaterialIcons name="arrow-back-ios" size={22} color="black" />
        </TouchableOpacity>
        <Text style={styles.heading}>All Ingredients</Text>
      </View>
      <ScrollView showsVerticalScrollIndicator={false} style={styles.container}>
        {groups.map((group) => (
          <View key={group.label} style={styles.ingredientsSection}>
            <View style={{ flexDirection: "row", gap: 10 }}>
              <Text style={styles.ingredientsSectionTitle}>{group.label}</Text>
            </View>
            <View style={styles.ingredientsSectionLayout}>
              <FlatList
                data={group.items}
                renderItem={renderItem}
                keyExtractor={(item) => item.id}
                numColumns={2}
                columnWrapperStyle={styles.row}
                contentContainerStyle={styles.listContent}
              />
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const { width } = Dimensions.get("window");
const CARD_GAP = 16;
const NUM_COLUMNS = 2;
const CARD_WIDTH = (width - CARD_GAP * (NUM_COLUMNS + 1)) / NUM_COLUMNS;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
  },

  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingLeft: 16,
    paddingRight: 16,
    paddingTop: 8,
    backgroundColor: "transparent",
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

  listContent: {
    padding: CARD_GAP,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: CARD_GAP,
  },

  ingredientsSection: {
    marginTop: 9,
  },

  arrowCircle: {
    height: 20,
    width: 20,
    backgroundColor: "#e7e7e7",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
  },

  ingredientsSectionTitle: {
    margin: 18,
    marginTop: 8,
    marginBottom: 0,
    fontSize: 16,
    fontWeight: 600,
    color: "#eb5757",
  },

  ingredientsSectionLayout: {
    display: "flex",
  },

  ingredientsCard: {
    height: 72,
    width: CARD_WIDTH,
    marginBottom: 0,
    backgroundColor: "#fffffe",
    borderRadius: 8,
    borderWidth: 2,
    borderColor: "#e7e7e7",
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

  deleteSlide: {
    justifyContent: "center",
    alignItems: "flex-end",
    paddingRight: 20,
    width: CARD_WIDTH,
    backgroundColor: "#bd0400",
    borderRadius: 8,
  },
});
