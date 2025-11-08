import React from "react";
import { FlatList, View } from "react-native";
import SliderItem from "./SliderItem";

interface SliderProps {
  data: any[];
  onDelete?: (name: string) => void;
}

const Slider: React.FC<SliderProps> = ({ data, onDelete }) => {
  return (
    <View>
      <FlatList
        data={data}
        renderItem={({ item, index }) => (
          <SliderItem item={item} index={index} onDelete={onDelete} />
        )}
        keyExtractor={(item, index) => item.name || index.toString()}
        horizontal
        showsHorizontalScrollIndicator={false}
        snapToAlignment="start"
        decelerationRate="fast"
        style={{ height: 86 }}
      />
    </View>
  );
};

export default Slider;
