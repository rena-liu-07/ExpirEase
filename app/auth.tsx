import { useAuth } from "@/lib/auth-context";
import { useRouter } from "expo-router";
import { useState } from "react";
import { KeyboardAvoidingView, Platform, StyleSheet, View } from "react-native";
import { Button, Text, TextInput, useTheme } from "react-native-paper";

export default function AuthScreen() {
  const [isSignUp, setIsSignUp] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>("");

  const theme = useTheme();
  const router = useRouter();

  const { login, signup } = useAuth();

  const handleAuth = async () => {
    if (
      (isSignUp && (!username || !email || !password)) ||
      (!isSignUp && (!username || !password))
    ) {
      setError("Please fill in all fileds.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be atleast 6 characters long");
      return;
    }

    setError(null);

    if (isSignUp) {
      const error = await signup(username, email, password);
      if (error) {
        setError(error);
        return;
      }
      // Successful signup, navigate to main app
      router.replace("/(tabs)");
    } else {
      const error = await login(username, password);
      if (error) {
        setError(error);
        return;
      }
      // Successful login, navigate to main app
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
          label="Username"
          autoCapitalize="none"
          mode="outlined"
          style={styles.input}
          onChangeText={setUsername}
        />

        <TextInput
          label="Email"
          autoCapitalize="none"
          keyboardType="email-address"
          placeholder="example@gmail.com"
          mode="outlined"
          style={[
            isSignUp ? { display: "flex" } : { display: "none" },
            styles.input,
          ]}
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
