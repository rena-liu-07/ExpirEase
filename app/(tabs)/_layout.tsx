import Entypo from "@expo/vector-icons/Entypo";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import { Tabs } from "expo-router";

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <MaterialCommunityIcons name="home" size={26} color="black" />
            ) : (
              <MaterialCommunityIcons
                name="home-outline"
                size={26}
                color="black"
              />
            );
          },
        }}
      />
      <Tabs.Screen
        name="saved-recipes"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <FontAwesome name="bookmark" size={24} color="black" />
            ) : (
              <FontAwesome name="bookmark-o" size={24} color="black" />
            );
          },
        }}
      />
      <Tabs.Screen
        name="new-ingredient"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <Entypo name="circle-with-plus" size={24} color="black" />
            ) : (
              <Entypo name="plus" size={24} color="black" />
            );
          },
        }}
      />
      <Tabs.Screen
        name="generate-recipe"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <Ionicons name="sparkles" size={24} color="black" />
            ) : (
              <Ionicons name="sparkles-outline" size={24} color="black" />
            );
          },
        }}
      />
      <Tabs.Screen
        name="sustainability-report"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <Ionicons name="leaf" size={21} color="black" />
            ) : (
              <Ionicons name="leaf-outline" size={21} color="black" />
            );
          },
        }}
      />
      <Tabs.Screen
        name="searched"
        options={{
          href: null,
          headerShown: false,
          tabBarShowLabel: false,
        }}
      />
      <Tabs.Screen
        name="photo-uploader"
        options={{
          href: null,
          headerShown: false,
          tabBarShowLabel: false,
        }}
      />
    </Tabs>
  );
}
