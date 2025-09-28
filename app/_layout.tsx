import { Stack } from "expo-router";
import { PaperProvider } from "react-native-paper";

// import { AuthProvider, useAuth } from "@/lib/auth-context";
// import { TransitionPresets } from "@react-navigation/stack";
// import { Stack, useRouter, useSegments } from "expo-router";
// import { useEffect, useState } from "react";
// import { GestureHandlerRootView } from "react-native-gesture-handler";
// import { SafeAreaProvider } from "react-native-safe-area-context";

// function RouteGuard({ children }: { children: React.ReactNode }) {
//   const router = useRouter();
//   const { user, isLoadingUser } = useAuth();
//   const [mounted, setMounted] = useState(false);
//   const segments = useSegments();

//   useEffect(() => {
//     setMounted(true);
//   }, []);

//   useEffect(() => {
//     const inAuthGroup = segments[0] === "auth";

//     if (mounted && !user && !inAuthGroup && !isLoadingUser) {
//       router.replace("/auth");
//     } else if (user && inAuthGroup && !isLoadingUser) {
//       router.replace("/(tabs)");
//     }
//   }, [mounted, user, segments]);

//   return <>{children}</>;
// }

export default function RootLayout() {
  return (
    <PaperProvider>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      </Stack>
    </PaperProvider>
  );
}
