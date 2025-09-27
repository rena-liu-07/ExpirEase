import { useAuth } from "@/lib/auth-context";
import { useRouter } from "expo-router";
import { useState } from "react";
import { KeyboardAvoidingView, Platform, StyleSheet, View } from "react-native";
import { Button, Text, TextInput, useTheme } from "react-native-paper";

export default function AuthScreen() {
  const [isSignUp, setIsSignUp] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>("");

  const theme = useTheme();
  const router = useRouter();

  const { signIn, signUp } = useAuth();

  const handleAuth = async () => {
    if (!email || !password) {
      setError("Please fill in all fileds.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be atleast 6 characters long");
      return;
    }

    setError(null);

    if (isSignUp) {
      const error = await signUp(email, password);
      if (error) {
        setError(error);
        return;
      }
    } else {
      const error = await signIn(email, password);
      if (error) {
        setError(error);
        return;
      }

      router.replace("/(tabs)");
    }
  };

  const handleSwitchMode = () => {
    setIsSignUp((prev) => !prev);
  };
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
    >
      {" "}
      <View style={styles.content}>
        <Text style={styles.title} variant="headlineMedium">
          {isSignUp ? "Create Account" : "Welcome Back"}
        </Text>

        <TextInput
          label="Email"
          autoCapitalize="none"
          keyboardType="email-address"
          placeholder="example@gmail.com"
          mode="outlined"
          style={styles.input}
          onChangeText={setEmail}
        />

        <TextInput
          label="Password"
          autoCapitalize="none"
          mode="outlined"
          secureTextEntry
          style={styles.input}
          onChangeText={setPassword}
        />

        {error && <Text style={{ color: theme.colors.error }}>{error}</Text>}

        <Button mode="contained" onPress={handleAuth} style={styles.button}>
          {isSignUp ? "Sign Up" : "Sign In"}
        </Button>

        <Button
          mode="text"
          onPress={handleSwitchMode}
          style={styles.switchModeButton}
        >
          {isSignUp
            ? "Already have an account? Sign In"
            : "Don't have an account? Sign Up"}
        </Button>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f5f5f5" },
  content: { flex: 1, padding: 16, justifyContent: "center" },
  title: { textAlign: "center", marginBottom: 24 },
  input: { marginBottom: 16 },
  button: { marginTop: 8 },
  switchModeButton: { marginTop: 16 },
  error: { color: "red", marginTop: 10 },
});

//

// import { useRouter } from "expo-router";
// import { useState } from "react";
// import { KeyboardAvoidingView, Platform, StyleSheet, View } from "react-native";
// import { Button, Text, TextInput, useTheme } from "react-native-paper";

// export default function AuthScreen() {
//   const [isSignUp, setIsSignUp] = useState(false);
//   const [username, setUsername] = useState("");
//   const [email, setEmail] = useState(""); // Only for signup
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const theme = useTheme();
//   const router = useRouter();

//   const handleAuth = async () => {
//     setError("");
//     if (!username || !password || (isSignUp && !email)) {
//       setError("Please fill in all fields.");
//       return;
//     }
//     if (password.length < 6) {
//       setError("Password must be at least 6 characters long");
//       return;
//     }
//     try {
//       const endpoint = isSignUp ? "/signup" : "/login";
//       const body = isSignUp
//         ? { username, email, password }
//         : { username, password };
//       const res = await fetch("http://localhost:5000/" + endpoint, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(body),
//       });
//       const data = await res.json();
//       if (res.ok && data.user_id) {
//         // Store user_id in async storage or context as needed
//         router.replace("/(tabs)");
//       } else {
//         setError(data.error || "Authentication failed");
//       }
//     } catch (e) {
//       setError("Network error");
//     }
//   };

//   return (
//     <KeyboardAvoidingView
//       behavior={Platform.OS === "ios" ? "padding" : "height"}
//       style={styles.container}
//     >
//       <View style={styles.content}>
//         <Text style={styles.title} variant="headlineMedium">
//           {isSignUp ? "Create Account" : "Welcome Back"}
//         </Text>
//         <TextInput
//           label="Username"
//           value={username}
//           onChangeText={setUsername}
//           style={styles.input}
//         />
//         {isSignUp && (
//           <TextInput
//             label="Email"
//             value={email}
//             onChangeText={setEmail}
//             style={styles.input}
//           />
//         )}
//         <TextInput
//           label="Password"
//           value={password}
//           onChangeText={setPassword}
//           secureTextEntry
//           style={styles.input}
//         />
//         {error ? <Text style={styles.error}>{error}</Text> : null}
//         <Button mode="contained" onPress={handleAuth} style={styles.button}>
//           {isSignUp ? "Sign Up" : "Log In"}
//         </Button>
//         <Button onPress={() => setIsSignUp((prev) => !prev)}>
//           {isSignUp ? "Already have an account? Log In" : "No account? Sign Up"}
//         </Button>
//       </View>
//     </KeyboardAvoidingView>
//   );
// }

// const styles = StyleSheet.create({
//   container: { flex: 1, backgroundColor: "#f5f5f5" },
//   content: { flex: 1, padding: 16, justifyContent: "center" },
//   title: { textAlign: "center", marginBottom: 24 },
//   input: { marginBottom: 16 },
//   button: { marginTop: 8 },
//   switchModeButton: { marginTop: 16 },
//   error: { color: "red", marginTop: 10 },
// });
