import Feather from "@expo/vector-icons/Feather";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useState } from "react";
import { Image, ScrollView, StyleSheet, TextInput, View } from "react-native";
import { Button, Card, Text } from "react-native-paper";
import Swiper from "react-native-swiper";

export default function SavedRecipesScreen() {
  const [search, setSearch] = useState("");

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
        />
      </View>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.ingredientsSection}>
          <View
            style={{
              flexDirection: "row",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <View style={{ flexDirection: "row", gap: 12 }}>
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
            <Card elevation={0} style={styles.ingredientsCard}>
              <View style={styles.cardImageContainer}>
                <Image
                  source={require("../../assets/images/icon.png")}
                  style={styles.cardImage}
                  resizeMode="cover"
                />
              </View>
              <View style={styles.cardTitleContainer}>
                <Text style={styles.cardName}>Sheppard's Pie</Text>
              </View>
            </Card>
          </Swiper>
        </View>
        <View style={styles.ingredientsSection}>
          <View
            style={{
              flexDirection: "row",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <View style={{ flexDirection: "row", gap: 12 }}>
              <Text style={styles.heading}>Favorites</Text>
              <View style={styles.arrowCircle}>
                <MaterialIcons
                  name="arrow-forward-ios"
                  size={15}
                  color="black"
                />
              </View>
            </View>
            <Button
              mode="text"
              style={{ marginRight: 18 }}
              // onPress={() => router.push("/index-see-all")}
            >
              See All
            </Button>
          </View>
          <Swiper
            style={styles.swiperContainer}
            showsButtons={false}
            showsPagination={false}
            loop={false}
          >
            <Card elevation={0} style={styles.ingredientsCard}>
              <View style={styles.cardImageContainer}>
                <Image
                  source={require("../../assets/images/icon.png")}
                  style={styles.cardImage}
                  resizeMode="cover"
                />
              </View>
              <View style={styles.cardTitleContainer}>
                <Text style={styles.cardName}>Sheppard's Pie</Text>
              </View>
            </Card>
          </Swiper>
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

  heading: {
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a1a",
  },

  ingredientsSection: {
    margin: 18,
    marginTop: 0,
  },

  arrowCircle: {
    height: 24,
    width: 24,
    backgroundColor: "#e7e7e7",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
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
    backgroundColor: "#f7f2fa",
    width: 164,
    height: 200,
    overflow: "hidden",
    padding: 0,
  },
  cardImageContainer: {
    height: 150, // 3/4 of 200
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
    height: 50, // 1/4 of 200
    justifyContent: "flex-start",
    paddingLeft: 10,
    paddingTop: 5,
    backgroundColor: "#f7f2fa",
  },
  cardName: {
    fontSize: 14,
    color: "#1a1a1a",
  },
});
