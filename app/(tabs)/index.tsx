import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { StyleSheet, TextInput, View } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import Swiper from "react-native-swiper";
// import "swiper/css";

export default function Index() {
  return (
    <View style={styles.container}>
      <TextInput
        placeholder="Search"
        underlineColorAndroid="transparent"
        style={styles.search}
      />
      <View style={styles.headingSection}>
        <Text style={styles.heading}>Expiring Soon</Text>
        <Button mode="text" style={{ marginRight: 18 }}>
          See All
        </Button>
      </View>
      <View style={styles.ingredientsSection}>
        <View style={{ flexDirection: "row", gap: 10 }}>
          <Text style={styles.ingredientsSectionTitle}>Expiring [Today]</Text>
          <MaterialIcons
            name="arrow-forward-ios"
            size={13}
            color="black"
            style={styles.arrow}
          />
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

  search: {
    margin: 18,
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 12,
    paddingRight: 16,
    backgroundColor: "#e7e7e7",
    fontSize: 18,
    color: "#828282",
    marginBottom: 24,
    borderRadius: 8,
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

  arrow: {
    height: 20,
    width: 20,
    backgroundColor: "#e7e7e7",
    borderRadius: 25,
    textAlign: "center",
  },

  ingredientsSectionTitle: {
    marginBottom: 12,
    fontSize: 16,
    fontWeight: 600,
    color: "#1a1a1a",
  },

  swiperContainer: {
    gap: 10,
  },

  ingredientsCard: {
    margin: 8,
    marginBottom: 18,
    borderRadius: 8,
    backgroundColor: "#f7f2fa",
    height: 61,
    width: 164,
  },

  cardTextContainer: {
    paddingBottom: 2,
    paddingLeft: 5,
    // textAlign: "left",
    // alignItems: "baseline",
    bottom: 0,
    right: 0,
  },

  cardCategory: {
    fontSize: 12,
    color: "#686666",
  },

  cardIngredient: {
    fontSize: 14,
    color: "#1a1a1a",
  },
});
