import React from "react";
import { FlatList, View } from "react-native";
import SliderItem from "./SliderItem";

interface SliderProps {
  data: any[];
}

const Slider: React.FC<SliderProps> = ({ data }) => {
  return (
    <View>
      <FlatList
        data={data}
        renderItem={({ item, index }) => (
          <SliderItem item={item} index={index} />
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
