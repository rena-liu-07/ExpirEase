// import { Stack } from "expo-router";

import { AuthProvider, useAuth } from "@/lib/auth-context";
import { Stack, useRouter, useSegments } from "expo-router";
import { useEffect, useState } from "react";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { PaperProvider } from "react-native-paper";
import { SafeAreaProvider } from "react-native-safe-area-context";

function RouteGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, setUser } = useAuth();
  const [mounted, setMounted] = useState(false);
  const segments = useSegments();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const inAuthGroup = segments[0] === "auth";

    if (mounted && !user && !inAuthGroup && !setUser) {
      router.replace("/auth");
    } else if (user && inAuthGroup && !setUser) {
      router.replace("/(tabs)");
    }
  }, [mounted, user, segments]);

  return <>{children}</>;
}

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <AuthProvider>
        <PaperProvider>
          <SafeAreaProvider>
            <RouteGuard>
              <Stack
                screenOptions={{
                  headerShown: false,
                  contentStyle: { backgroundColor: "#fcfcfa" },
                }}
              >
                <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
                <Stack.Screen
                  name="index-see-all"
                  options={{
                    headerShown: false,
                  }}
                />
                <Stack.Screen
                  name="profile-settings"
                  options={{
                    headerShown: false,
                  }}
                />
              </Stack>
            </RouteGuard>
          </SafeAreaProvider>
        </PaperProvider>
      </AuthProvider>
    </GestureHandlerRootView>
  );
}

// import { Stack } from "expo-router";
// import { PaperProvider } from "react-native-paper";

// export default function RootLayout() {
//   return (
//     <PaperProvider>
//       <Stack screenOptions={{ headerShown: false }}>
//         <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
//       </Stack>
//     </PaperProvider>
//   );
// }
