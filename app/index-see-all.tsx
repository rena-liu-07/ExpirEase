import {
  Dimensions,
  FlatList,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";
import { Card, Text } from "react-native-paper";

export default function IndexSeeAllScreen() {
  return (
    <ScrollView showsVerticalScrollIndicator={false} style={styles.container}>
      <View style={styles.ingredientsSection}>
        <View style={{ flexDirection: "row", gap: 16 }}>
          <Text style={styles.ingredientsSectionTitle}>Expiring [Today]</Text>
        </View>
        <View style={styles.ingredientsSectionLayout}>
          <FlatList
            data={DATA}
            renderItem={renderItem}
            keyExtractor={(item) => item.id}
            numColumns={2}
            columnWrapperStyle={styles.row}
            contentContainerStyle={styles.listContent}
          />
        </View>
      </View>
    </ScrollView>
  );
}

const DATA = [
  { id: "1", category: "Fruit", ingredient: "Apple" },
  { id: "2", category: "Vegetable", ingredient: "Carrot" },
  { id: "3", category: "Dairy", ingredient: "Milk" },
  { id: "4", category: "Meat", ingredient: "Chicken" },
  { id: "5", category: "Grain", ingredient: "Rice" },
  { id: "6", category: "Snack", ingredient: "Chips" },
];

const renderItem = ({ item }) => (
  <Card style={styles.ingredientsCard} elevation={0}>
    <Card.Content style={styles.cardTextContainer}>
      <Text style={styles.cardCategory}>{item.category}</Text>
      <Text style={styles.cardIngredient}>{item.ingredient}</Text>
    </Card.Content>
  </Card>
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
    marginTop: 18,
    marginBottom: 18,
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
