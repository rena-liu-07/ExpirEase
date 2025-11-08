// SliderItem.tsx
import Feather from "@expo/vector-icons/Feather";
import React from "react";
import { StyleSheet, View } from "react-native";
import { Swipeable } from "react-native-gesture-handler";
import { Card, Text } from "react-native-paper";

interface SliderItemProps {
  item: any;
  index?: number;
  onDelete?: (name: string) => void;
}

const SliderItem: React.FC<SliderItemProps> = ({ item, onDelete }) => {
  const renderRightActions = () => (
    <View style={styles.deleteSlide}>
      <Feather name="trash-2" size={24} color="white" />
    </View>
  );

  const handleSwipeOpen = () => {
    if (onDelete) {
      onDelete(item.name);
    }
  };

  if (!onDelete) {
    // If no delete handler provided, render without swipe
    return (
      <Card key={item.name} elevation={0} style={styles.ingredientsCard}>
        <Card.Content style={styles.cardTextContainer}>
          <Text style={styles.cardCategory}>{item.category}</Text>
          <Text style={styles.cardIngredient}>{item.name}</Text>
        </Card.Content>
      </Card>
    );
  }

  return (
    <Swipeable
      renderRightActions={renderRightActions}
      onSwipeableOpen={handleSwipeOpen}
    >
      <Card key={item.name} elevation={0} style={styles.ingredientsCard}>
        <Card.Content style={styles.cardTextContainer}>
          <Text style={styles.cardCategory}>{item.category}</Text>
          <Text style={styles.cardIngredient}>{item.name}</Text>
        </Card.Content>
      </Card>
    </Swipeable>
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
    backgroundColor: "#fffffe",
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
    backgroundColor: "#ff4444",
    justifyContent: "center",
    alignItems: "center",
    width: 80,
    height: 72,
    borderRadius: 8,
    margin: 8,
    marginBottom: 26,
    marginRight: 16,
  },
});

export default SliderItem;
