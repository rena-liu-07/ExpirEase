import Feather from "@expo/vector-icons/Feather";
import { useEffect, useState } from "react";
import {
  Dimensions,
  FlatList,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";
import { Swipeable } from "react-native-gesture-handler";
import { Card, Text } from "react-native-paper";

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

function groupIngredients(ingredients) {
  const today = new Date();
  const used = new Set();
  const groups = EXPIRY_GROUPS.map((g) => ({ ...g, items: [] }));

  for (const ing of ingredients) {
    const exp = new Date(ing.expiration);
    const days = Math.floor((exp - today) / (1000 * 60 * 60 * 24));
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

const [ingredients, setIngredients] = useState([]);

const handleDelete = async (name) => {
  await fetch(
    `http://YOUR_IP:5000/delete-ingredient?name=${encodeURIComponent(name)}`,
    {
      method: "DELETE",
    }
  );
  setIngredients((prev) => prev.filter((item) => item.name !== name));
};

export default function IndexSeeAllScreen() {
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/all-ingredients")
      .then((res) => res.json())
      .then((data) => setGroups(groupIngredients(data)));
  }, []);

  return (
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
  );
}

const renderItem = ({ item }) => (
  <Swipeable
    renderRightActions={() => (
      <View
        style={{
          justifyContent: "center",
          alignItems: "center",
          width: 80,
          backgroundColor: "red",
        }}
      >
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

const { width } = Dimensions.get("window");
const CARD_GAP = 16;
const NUM_COLUMNS = 2;
const CARD_WIDTH = (width - CARD_GAP * (NUM_COLUMNS + 1)) / NUM_COLUMNS;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
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
    marginBottom: 0,
    fontSize: 16,
    fontWeight: 600,
    color: "#1a1a1a",
  },

  ingredientsSectionLayout: {
    display: "flex",
  },

  ingredientsCard: {
    borderRadius: 8,
    backgroundColor: "#f7f2fa",
    height: 61,
    width: CARD_WIDTH,
    marginBottom: 0,
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
