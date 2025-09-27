import Entypo from "@expo/vector-icons/Entypo";
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
              <MaterialCommunityIcons name="home" size={24} color="black" />
            ) : (
              <MaterialCommunityIcons
                name="home-outline"
                size={24}
                color="black"
              />
            );
          },
        }}
      ></Tabs.Screen>
      <Tabs.Screen
        name="new-ingredient"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <Entypo name="circle-with-plus" size={23} color="black" />
            ) : (
              <Entypo name="plus" size={23} color="black" />
            );
          },
        }}
      ></Tabs.Screen>
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
      ></Tabs.Screen>
      <Tabs.Screen
        name="photo-uploader"
        options={{
          headerShown: false,
          tabBarShowLabel: false,
          tabBarIcon: ({ focused }) => {
            return focused ? (
              <Ionicons name="cloud-upload" size={24} color="black" />
            ) : (
              <Ionicons name="cloud-upload-outline" size={24} color="black" />
            );
          },
        }}
      ></Tabs.Screen>
    </Tabs>
  );
}
