import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useState } from "react";
import {
  FlatList,
  Image,
  ScrollView,
  StyleSheet,
  TextInput,
  View,
} from "react-native";
import { Card, Text } from "react-native-paper";
import Swiper from "react-native-swiper";

export default function SavedRecipesScreen() {
  const [search, setSearch] = useState("");

  // Mock data for favorite recipes
  const favoriteRecipes = [
    {
      id: "1",
      title: "Classic Lasagna",
      image: require("../../assets/images/icon.png"),
    },
    {
      id: "2",
      title: "Vegan Buddha Bowl",
      image: require("../../assets/images/partial-react-logo.png"),
    },
    {
      id: "3",
      title: "Chicken Alfredo",
      image: require("../../assets/images/react-logo.png"),
    },
    {
      id: "4",
      title: "Berry Smoothie",
      image: require("../../assets/images/splash-icon.png"),
    },
  ];

  // Mock data for recent recipes (swiper)
  const recentRecipes = [
    {
      id: "a",
      title: "Sheppard's Pie",
      image: require("../../assets/images/icon.png"),
    },
    {
      id: "b",
      title: "Avocado Toast",
      image: require("../../assets/images/partial-react-logo.png"),
    },
    {
      id: "c",
      title: "Miso Ramen",
      image: require("../../assets/images/react-logo.png"),
    },
    {
      id: "d",
      title: "Fruit Parfait",
      image: require("../../assets/images/splash-icon.png"),
    },
  ];

  const renderFavoriteItem = ({ item }) => (
    <Card elevation={0} style={styles.ingredientsCard}>
      <View style={styles.cardImageContainer}>
        <Image
          source={item.image}
          style={styles.cardImage}
          resizeMode="cover"
        />
      </View>
      <View style={styles.cardTitleContainer}>
        <Text style={styles.cardName} numberOfLines={2}>
          {item.title}
        </Text>
      </View>
    </Card>
  );

  const renderRecipeCard = (item) => (
    <Card elevation={0} style={styles.ingredientsCard}>
      <View style={styles.cardImageContainer}>
        <Image
          source={item.image}
          style={styles.cardImage}
          resizeMode="cover"
        />
      </View>
      <View style={styles.cardTitleContainer}>
        <Text style={styles.cardName} numberOfLines={2}>
          {item.title}
        </Text>
      </View>
    </Card>
  );

  return (
    <View style={styles.container}>
      {/* Search */}
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
        />
      </View>

      {/* Scrollable Content */}
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Recent Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <View
              style={{ flexDirection: "row", alignItems: "center", gap: 12 }}
            >
              <Text style={styles.heading}>Recent</Text>
              <View style={styles.arrowCircle}>
                <MaterialIcons
                  name="arrow-forward-ios"
                  size={15}
                  color="black"
                />
              </View>
            </View>
          </View>

          <Swiper
            style={styles.swiperContainer}
            showsButtons={false}
            showsPagination={false}
            loop={false}
          >
            {recentRecipes.map((item) => (
              <View key={item.id} style={styles.swiperSlide}>
                {renderRecipeCard(item)}
              </View>
            ))}
          </Swiper>
        </View>

        {/* Favorites Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.heading}>Favorites</Text>
          </View>
          <FlatList
            data={favoriteRecipes}
            renderItem={renderFavoriteItem}
            keyExtractor={(item) => item.id}
            numColumns={2}
            columnWrapperStyle={styles.row}
            contentContainerStyle={styles.listContent}
            scrollEnabled={false}
          />
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
  },

  // Search
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
    paddingVertical: 8,
    paddingRight: 18,
    fontSize: 18,
    color: "#828282",
    backgroundColor: "transparent",
  },

  // Sections
  section: {
    marginBottom: 18, // spacing between sections
  },
  sectionHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 18,
    marginBottom: 18,
    marginTop: 8,
  },
  heading: {
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a1a",
  },

  arrowCircle: {
    height: 24,
    width: 24,
    backgroundColor: "#e7e7e7",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },

  // Swiper
  swiperContainer: {
    height: 200,
  },
  swiperSlide: {
    paddingHorizontal: 18,
  },

  // Cards
  ingredientsCard: {
    borderRadius: 8,
    backgroundColor: "#f7f2fa",
    width: 164,
    height: 150,
    overflow: "hidden",
  },
  cardImageContainer: {
    height: 100,
    width: "100%",
    backgroundColor: "#e0e0e0",
  },
  cardImage: {
    width: "100%",
    height: "100%",
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  cardTitleContainer: {
    height: 50,
    justifyContent: "flex-start",
    paddingLeft: 10,
    paddingTop: 10,
    backgroundColor: "#f7f2fa",
  },
  cardName: {
    fontSize: 16,
    color: "#1a1a1a",
  },

  // Favorites Grid
  listContent: {
    paddingHorizontal: 18,
  },
  row: {
    flex: 1,
    justifyContent: "space-between",
    marginBottom: 18,
  },
});
