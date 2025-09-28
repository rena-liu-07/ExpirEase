import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import React, { useMemo } from "react";
import {
  FlatList,
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from "react-native";
import { Card } from "react-native-paper";
import Swiper from "react-native-swiper";

// Recipe interface
interface Recipe {
  id: string;
  title: string;
  image: any; // can be require() or string
}

// Helper to chunk array into pairs
function chunkPairs<T>(arr: T[]): (T | null)[][] {
  const out: (T | null)[][] = [];
  for (let i = 0; i < arr.length; i += 2) {
    out.push([arr[i], arr[i + 1] ?? null]);
  }
  return out;
}

const renderRecipeCard = ({ item }: { item: Recipe | null }) => {
  if (!item) {
    return null;
  }

  return (
    <Card elevation={0} style={styles.ingredientsCard}>
      <View style={styles.cardImageContainer}>
        <Image
          source={
            typeof item.image === "string" ? { uri: item.image } : item.image
          }
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
};

const renderFavoriteItem = ({ item }: { item: Recipe | null }) => {
  if (!item) {
    return null;
  }

  return (
    <Card elevation={0} style={styles.ingredientsCard}>
      <View style={styles.cardImageContainer}>
        <Image
          source={
            typeof item.image === "string" ? { uri: item.image } : item.image
          }
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
};

interface SavedRecipesScreenProps {
  favoriteRecipes?: Recipe[];
  recentRecipes?: Recipe[];
}

export default function SavedRecipesScreen({
  favoriteRecipes = [
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
  ],

  // Mock data for recent recipes (swiper)
  recentRecipes = [
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
  ],
}: SavedRecipesScreenProps) {
  const { width: W } = useWindowDimensions();

  const SIDE_PADDING = 16; // padding on left/right edges
  const GAP = 16; // gap between cards

  // Compute card width so that 2 cards + gap + edge paddings fit the screen
  const cardWidth = (W - SIDE_PADDING * 2 - GAP) / 2;

  const slides = useMemo(() => chunkPairs(recentRecipes), [recentRecipes]);

  // wrapper for consistent width
  const FavoriteCardWrapper = ({ item }: { item: Recipe }) => {
    return (
      <View style={{ width: cardWidth }}>{renderFavoriteItem({ item })}</View>
    );
  };

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
          returnKeyType="search"
        />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Recent section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.heading}>Recent</Text>
            <View style={styles.arrowCircle}>
              <MaterialIcons name="arrow-forward-ios" size={13} color="black" />
            </View>
          </View>

          <View style={{ height: 220, paddingHorizontal: SIDE_PADDING }}>
            <Swiper showsButtons={false} showsPagination={false} loop={false}>
              {slides.map((pair, idx) => (
                <View
                  key={idx}
                  style={{
                    flexDirection: "row",
                    justifyContent: "space-between",
                  }}
                >
                  {pair.map((item, i) => (
                    <View key={i} style={{ width: cardWidth }}>
                      {renderRecipeCard({ item })}
                    </View>
                  ))}
                </View>
              ))}
            </Swiper>
          </View>
        </View>

        {/* Favorites section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.heading}>Favorites</Text>
          </View>

          <FlatList
            data={favoriteRecipes}
            renderItem={({ item }) => <FavoriteCardWrapper item={item} />}
            keyExtractor={(item) => item.id}
            numColumns={2}
            // ensure two columns align with same side padding & gap
            columnWrapperStyle={{
              justifyContent: "space-between",
              paddingHorizontal: SIDE_PADDING,
              marginBottom: 16,
            }}
            contentContainerStyle={{ paddingTop: 0, paddingBottom: 24 }}
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
    marginHorizontal: 16, // use 16 to match card side padding
    marginTop: 16,
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
    paddingRight: 16,
    fontSize: 18,
    color: "#828282",
    backgroundColor: "transparent",
  },

  // Sections
  section: {
    marginBottom: 18,
  },
  sectionHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    marginBottom: 12,
    marginTop: 8,
  },
  heading: {
    fontSize: 24,
    fontWeight: "700",
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

  // swiper slide (wrapper that Swiper expects)
  slide: {
    flex: 1,
    justifyContent: "center",
  },
  slideRow: {
    flexDirection: "row",
    justifyContent: "space-between", // creates the GAP between the two card wrappers
    alignItems: "flex-start",
  },

  // Cards (NO fixed width; width is '100%' so parent wrapper controls final width)
  ingredientsCard: {
    borderRadius: 8,
    backgroundColor: "#f7f2fa",
    width: "100%", // let parent wrapper set actual width
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
});
