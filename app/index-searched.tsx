import Feather from "@expo/vector-icons/Feather";
import { StyleSheet, TextInput, View } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import Swiper from "react-native-swiper";
// import "swiper/css";

export default function IndexSearchedScreen() {
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
        />
      </View>
      <View style={styles.headingSection}>
        <Text style={styles.heading}>Expiring Soon</Text>
        <Button mode="text" style={{ marginRight: 18 }}>
          See All
        </Button>
      </View>
      <View style={styles.ingredientsSection}>
        <View style={{ flexDirection: "row", gap: 10 }}>
          <Text style={styles.ingredientsSectionTitle}>Expiring [Today]</Text>
        </View>
        <Swiper
          style={styles.swiperContainer}
          showsButtons={false}
          loop={false}
        >
          <Card elevation={0} style={styles.ingredientsCard}>
            <Card.Content style={styles.cardTextContainer}>
              <Text style={styles.cardCategory}>[Category]</Text>
              <Text style={styles.cardIngredient}>[Ingredient]</Text>
            </Card.Content>
          </Card>
          <Card elevation={0} style={styles.ingredientsCard}>
            <Card.Content style={styles.cardTextContainer}>
              <Text style={styles.cardCategory}>[Category]</Text>
              <Text style={styles.cardIngredient}>[Ingredient]</Text>
            </Card.Content>
          </Card>
          <Card elevation={0} style={styles.ingredientsCard}>
            <Card.Content style={styles.cardTextContainer}>
              <Text style={styles.cardCategory}>[Category]</Text>
              <Text style={styles.cardIngredient}>[Ingredient]</Text>
            </Card.Content>
          </Card>
        </Swiper>
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
    // margin: 18,
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
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  heading: {
    margin: 18,
    marginBottom: 18,
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
    backgroundColor: "#e7e7e7",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
  },

  ingredientsSectionTitle: {
    marginBottom: 12,
    fontSize: 16,
    fontWeight: 600,
    color: "#1a1a1a",
  },

  swiperContainer: {
    // gap: 10,
  },

  ingredientsCard: {
    margin: 8,
    marginBottom: 18,
    marginRight: 16,
    borderRadius: 8,
    backgroundColor: "#f7f2fa",
    height: 61,
    width: 164,
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
