import Feather from "@expo/vector-icons/Feather";
import { StyleSheet, TextInput, View } from "react-native";
import { Text } from "react-native-paper";
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
        <Text style={styles.heading}>[ingredient name]</Text>
        <Text style={styles.subheading}>[type, category]</Text>
        <Text style={styles.expirationDate}>[Expiration: date]</Text>
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
    margin: 18,
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
    margin: 18,
  },

  heading: {
    marginBottom: 8,
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a1a",
  },

  subheading: {
    marginBottom: 8,
    fontSize: 16,
  },

  expirationDate: {
    marginBottom: 8,
    fontSize: 16,
    fontWeight: 700,
  },
});
