import { Stack } from "expo-router";

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
    // <GestureHandlerRootView style={{ flex: 1 }}>
    //   <AuthProvider>
    //     <PaperProvider>
    //       <SafeAreaProvider>
    //         <RouteGuard>
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
    //         </RouteGuard>
    //       </SafeAreaProvider>
    //     </PaperProvider>
    //   </AuthProvider>
    // </GestureHandlerRootView>
  );
}
