import { Tabs } from "expo-router";

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: "Home" }}></Tabs.Screen>
      <Tabs.Screen
        name="new-ingredient"
        options={{ title: "New Ingredient" }}
      ></Tabs.Screen>
      <Tabs.Screen
        name="sustainability-report"
        options={{ title: "Sustainability Report" }}
      ></Tabs.Screen>
    </Tabs>
  );
}
