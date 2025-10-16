// SliderItem.tsx
import React from "react";
import { StyleSheet } from "react-native";
import { Card, Text } from "react-native-paper";

const SliderItem = ({ item }: { item: any }) => {
  return (
    <Card key={item.name} elevation={0} style={styles.ingredientsCard}>
      <Card.Content style={styles.cardTextContainer}>
        <Text style={styles.cardCategory}>{item.category}</Text>
        <Text style={styles.cardIngredient}>{item.name}</Text>
      </Card.Content>
    </Card>
  );
};

const styles = StyleSheet.create({
  ingredientsCard: {
    margin: 8,
    marginBottom: 26,
    marginRight: 16,
    borderRadius: 8,
    height: 72,
    width: 164,
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "#e0e0e0",
    elevation: 3,
    shadowColor: "#686666",
    shadowOpacity: 0.5,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 3,
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

export default SliderItem;
