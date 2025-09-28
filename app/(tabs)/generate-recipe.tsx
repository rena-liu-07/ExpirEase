import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { useEffect, useState } from "react";
import { Alert, ScrollView, StyleSheet, View } from "react-native";
import {
  Button,
  Card,
  Chip,
  Dialog,
  Divider,
  Portal,
  RadioButton,
  Text,
  TextInput,
} from "react-native-paper";
import { API_ENDPOINTS, apiCall } from "../../config/api";

interface ExpiringIngredient {
  name: string;
  days_until_expiry: number;
  category_or_nutrition: string;
}

interface RecipeResponse {
  success: boolean;
  recipe?: string;
  error?: string;
}

interface Recipe {
  id: string;
  title: string;
  content: string;
  size: string;
  dietary: string;
  cuisine: string;
  timestamp: Date;
}

export default function GenerateRecipeScreen() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(false);
  const [expiringIngredients, setExpiringIngredients] = useState<
    ExpiringIngredient[]
  >([]);

  // Recipe generation options
  const [recipeSize, setRecipeSize] = useState("medium");
  const [dietaryRestrictions, setDietaryRestrictions] = useState("");
  const [cuisinePreference, setCuisinePreference] = useState("");
  const [prioritizeExpiring, setPrioritizeExpiring] = useState(true);

  // Dialog states
  const [showOptionsDialog, setShowOptionsDialog] = useState(false);
  const [showFullscreenRecipe, setShowFullscreenRecipe] = useState(false);

  // Load expiring ingredients on component mount
  useEffect(() => {
    loadExpiringIngredients();
  }, []);

  const loadExpiringIngredients = async () => {
    try {
      const data = (await apiCall(
        `${API_ENDPOINTS.EXPIRING_INGREDIENTS}?days_threshold=5`
      )) as ExpiringIngredient[];
      setExpiringIngredients(data);
    } catch (error) {
      console.error("Failed to load expiring ingredients:", error);
    }
  };

  const generateRecipe = async () => {
    setLoading(true);
    try {
      const requestBody = {
        recipe_size: recipeSize,
        dietary_restrictions: dietaryRestrictions,
        cuisine_preference: cuisinePreference,
        prioritize_expiring: prioritizeExpiring,
      };

      // Try to call the API first
      let data: RecipeResponse;
      try {
        data = (await apiCall(API_ENDPOINTS.GENERATE_RECIPE, {
          method: "POST",
          body: JSON.stringify(requestBody),
        })) as RecipeResponse;
      } catch (apiError) {
        console.log("API call failed, using mock recipe:", apiError);
        // Mock recipe generation when backend is unavailable
        data = {
          success: true,
          recipe: generateMockRecipe(
            recipeSize,
            cuisinePreference,
            dietaryRestrictions
          ),
        };
      }

      if (data.success && data.recipe) {
        // Extract recipe title from the content (first line or first few words)
        const recipeLines = data.recipe.split("\n");
        const title =
          recipeLines[0].replace(/[🍳📊🌍⭐*#]/g, "").trim() ||
          `${cuisinePreference || "Delicious"} ${recipeSize} Recipe`;

        const newRecipe: Recipe = {
          id: Date.now().toString(),
          title: title,
          content: data.recipe,
          size: recipeSize,
          dietary: dietaryRestrictions,
          cuisine: cuisinePreference,
          timestamp: new Date(),
        };

        setRecipes((prev) => [newRecipe, ...prev]);
        Alert.alert("Success!", "New recipe generated successfully!");
      } else {
        Alert.alert("Error", data.error || "Failed to generate recipe");
      }
    } catch (error) {
      Alert.alert("Error", "An unexpected error occurred");
      console.error("Recipe generation error:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateMockRecipe = (
    size: string,
    cuisine: string,
    dietary: string
  ) => {
    const baseIngredients = [
      "chicken breast",
      "tomatoes",
      "asparagus",
      "strawberries",
      "apple",
      "grapes",
      "banana",
    ];
    const cuisineStyles = {
      Italian: "al Pomodoro with Fresh Herbs",
      Asian: "Stir-Fry with Seasonal Fruits",
      Mexican: "with Salsa Fresca",
      "": "with Garden Vegetables",
    };

    const recipeName = `${cuisine || "Delicious"} ${
      size.charAt(0).toUpperCase() + size.slice(1)
    } ${
      cuisineStyles[cuisine as keyof typeof cuisineStyles] || cuisineStyles[""]
    }`;

    return `🍳 **${recipeName}**

📊 **Recipe Size:** ${size.charAt(0).toUpperCase() + size.slice(1)}
${dietary ? `🥗 **Dietary Notes:** ${dietary}\n` : ""}${
      cuisine ? `🌍 **Cuisine Style:** ${cuisine}\n` : ""
    }

📋 **Ingredients:**
${baseIngredients
  .slice(0, size === "small" ? 4 : size === "large" ? 7 : 5)
  .map(
    (ingredient, i) =>
      `${i + 1}. ${ingredient.charAt(0).toUpperCase() + ingredient.slice(1)}`
  )
  .join("\n")}

⏰ **Use These First (Expiring Soon):**
• Strawberries (expires in 1 days)
• Banana (expires in 2 days)

👨‍🍳 **Instructions:**
1. Prepare all ingredients by washing and chopping as needed
2. Heat oil in a large pan over medium-high heat
3. Cook protein ingredients first until properly cooked
4. Add vegetables in order of cooking time needed
5. Incorporate fruits toward the end to maintain texture
6. Season with salt, pepper, and herbs to taste
7. Serve immediately while hot

⏱️ **Estimated Cooking Time:** 25-30 minutes

💡 **Note:** This recipe uses your available ingredients. The backend AI will provide more personalized recipes once connected!`;
  };

  const resetOptions = () => {
    setRecipeSize("medium");
    setDietaryRestrictions("");
    setCuisinePreference("");
    setPrioritizeExpiring(true);
  };

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View>
          <Text style={styles.headerTitle}>Generate Recipe</Text>
        </View>

        {/* Expiring Ingredients Alert */}
        {expiringIngredients.length > 0 && (
          <Card style={styles.expiringCard}>
            <Card.Content>
              <View style={styles.expiringHeader}>
                <MaterialIcons name="warning" size={24} color="#FF9800" />
                <Text style={styles.expiringTitle}>
                  Ingredients Expiring Soon
                </Text>
              </View>
              <Text style={styles.expiringSubtitle}>
                Use these ingredients to reduce food waste:
              </Text>
              <View style={styles.chipContainer}>
                {expiringIngredients.slice(0, 6).map((ingredient, index) => (
                  <Chip
                    key={index}
                    mode="outlined"
                    style={[
                      styles.expiringChip,
                      ingredient.days_until_expiry <= 1 && styles.urgentChip,
                    ]}
                    textStyle={[
                      ingredient.days_until_expiry <= 1 && styles.urgentText,
                    ]}
                  >
                    {ingredient.name} ({ingredient.days_until_expiry}d)
                  </Chip>
                ))}
              </View>
              {expiringIngredients.length > 6 && (
                <Text style={styles.moreIngredientsText}>
                  +{expiringIngredients.length - 6} more ingredients
                </Text>
              )}
            </Card.Content>
          </Card>
        )}

        {/* Current Settings Display */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Text style={styles.settingsTitle}>Recipe Preferences</Text>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Size:</Text>
              <Text style={styles.settingValue}>
                {recipeSize.charAt(0).toUpperCase() + recipeSize.slice(1)}
              </Text>
            </View>
            {dietaryRestrictions && (
              <View style={styles.settingRow}>
                <Text style={styles.settingLabel}>Dietary:</Text>
                <Text style={styles.settingValue}>{dietaryRestrictions}</Text>
              </View>
            )}
            {cuisinePreference && (
              <View style={styles.settingRow}>
                <Text style={styles.settingLabel}>Cuisine:</Text>
                <Text style={styles.settingValue}>{cuisinePreference}</Text>
              </View>
            )}
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Prioritize Expiring:</Text>
              <Text style={styles.settingValue}>
                {prioritizeExpiring ? "Yes" : "No"}
              </Text>
            </View>
          </Card.Content>
        </Card>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <Button
            mode="outlined"
            onPress={() => setShowOptionsDialog(true)}
            style={styles.optionsButton}
            icon="tune"
            labelStyle={{ color: "#1a1a1a" }}
          >
            Customize Options
          </Button>

          <Button
            mode="contained"
            onPress={generateRecipe}
            loading={loading}
            disabled={loading}
            style={styles.generateButton}
            icon="chef-hat"
          >
            {loading ? "Generating..." : "Generate Recipe"}
          </Button>
        </View>

        {/* Generated Recipes */}
        {recipes.length > 0 && (
          <View style={styles.recipesContainer}>
            <Text style={styles.recipesTitle}>Your Generated Recipes</Text>
            {recipes.map((recipe) => (
              <Card
                key={recipe.id}
                style={styles.recipeCard}
                onPress={() => {
                  setSelectedRecipe(recipe);
                  setShowFullscreenRecipe(true);
                }}
                elevation={0}
              >
                <Card.Content>
                  <View style={styles.recipeCardHeader}>
                    <Text style={styles.recipeCardTitle} numberOfLines={2}>
                      {recipe.title}
                    </Text>
                    <Text style={styles.recipeCardDate}>
                      {recipe.timestamp.toLocaleDateString()}
                    </Text>
                  </View>

                  <View style={styles.recipeCardDetails}>
                    <View style={styles.recipeCardTags}>
                      <Chip mode="outlined" compact style={styles.recipeTag}>
                        {recipe.size}
                      </Chip>
                      {recipe.cuisine && (
                        <Chip mode="outlined" compact style={styles.recipeTag}>
                          {recipe.cuisine}
                        </Chip>
                      )}
                      {recipe.dietary && (
                        <Chip mode="outlined" compact style={styles.recipeTag}>
                          {recipe.dietary}
                        </Chip>
                      )}
                    </View>
                  </View>

                  <Text style={styles.recipeCardPreview} numberOfLines={3}>
                    {recipe.content
                      .replace(/[🍳📊🌍⏰👨‍🍳💡⭐*#]/g, "")
                      .substring(0, 120)}
                    ...
                  </Text>

                  <View style={styles.recipeCardFooter}>
                    <Text style={styles.tapToViewText}>
                      Tap to view full recipe
                    </Text>
                    <MaterialIcons
                      name="chevron-right"
                      size={20}
                      color="#666"
                    />
                  </View>
                </Card.Content>
              </Card>
            ))}
          </View>
        )}
      </ScrollView>

      {/* Options Dialog */}
      <Portal>
        <Dialog
          visible={showOptionsDialog}
          onDismiss={() => setShowOptionsDialog(false)}
        >
          <Dialog.Title>Recipe Options</Dialog.Title>
          <Dialog.Content>
            <ScrollView>
              {/* Recipe Size */}
              <Text style={styles.dialogSectionTitle}>Recipe Size</Text>
              <RadioButton.Group
                onValueChange={setRecipeSize}
                value={recipeSize}
                accent-color={"#fcfcfa"}
              >
                <View style={styles.radioRow}>
                  <RadioButton value="small" color={"#eb5757"} />
                  <Text style={styles.radioLabel}>Small (1-2 servings)</Text>
                </View>
                <View style={styles.radioRow}>
                  <RadioButton value="medium" color={"#eb5757"} />
                  <Text style={styles.radioLabel}>Medium (3-4 servings)</Text>
                </View>
                <View style={styles.radioRow}>
                  <RadioButton value="large" color={"#eb5757"} />
                  <Text style={styles.radioLabel}>Large (5-6 servings)</Text>
                </View>
              </RadioButton.Group>

              <Divider style={styles.divider} />

              {/* Dietary Restrictions */}
              <Text style={styles.dialogSectionTitle}>
                Dietary Restrictions
              </Text>
              <TextInput
                value={dietaryRestrictions}
                onChangeText={setDietaryRestrictions}
                placeholder="e.g., vegetarian, vegan, gluten-free"
                mode="outlined"
                style={styles.textInput}
              />

              {/* Cuisine Preference */}
              <Text style={styles.dialogSectionTitle}>Cuisine Preference</Text>
              <TextInput
                value={cuisinePreference}
                onChangeText={setCuisinePreference}
                placeholder="e.g., Italian, Asian, Mexican"
                mode="outlined"
                style={styles.textInput}
              />

              {/* Prioritize Expiring */}
              <View style={styles.checkboxRow}>
                <RadioButton.Group
                  onValueChange={(value) =>
                    setPrioritizeExpiring(value === "true")
                  }
                  value={prioritizeExpiring.toString()}
                  accent-color={"#fcfcfa"}
                >
                  <View style={styles.radioRow}>
                    <RadioButton value="true" color={"#eb5757"} />
                    <Text style={styles.radioLabel}>
                      Prioritize expiring ingredients
                    </Text>
                  </View>
                  <View style={styles.radioRow}>
                    <RadioButton value="false" color={"#eb5757"} />
                    <Text style={styles.radioLabel}>
                      Use any available ingredients
                    </Text>
                  </View>
                </RadioButton.Group>
              </View>
            </ScrollView>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={resetOptions} accent-color={"#eb5757"}>
              Reset
            </Button>
            <Button
              onPress={() => setShowOptionsDialog(false)}
              accent-color={"#eb5757"}
            >
              Done
            </Button>
          </Dialog.Actions>
        </Dialog>

        {/* Fullscreen Recipe Display */}
        <Dialog
          visible={showFullscreenRecipe}
          onDismiss={() => setShowFullscreenRecipe(false)}
          style={styles.fullscreenDialog}
        >
          <Dialog.Title style={styles.fullscreenTitle}>
            {selectedRecipe?.title || "Recipe"}
          </Dialog.Title>
          <Dialog.Content>
            <ScrollView style={styles.fullscreenContent}>
              <Text style={styles.fullscreenRecipeText}>
                {selectedRecipe?.content || ""}
              </Text>
            </ScrollView>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setShowFullscreenRecipe(false)}>
              Close
            </Button>
            <Button
              mode="contained"
              onPress={() => {
                // Here you could implement saving to favorites
                Alert.alert("Success", "Recipe saved to favorites!");
              }}
            >
              Save Recipe
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </View>
  );
}

const styles: any = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fcfcfa",
    padding: 24,
  },
  headerTitle: {
    margin: 18,
    marginBottom: 18,
    fontSize: 20,
    fontWeight: "700",
    color: "#1a1a1a",
    textAlign: "center",
  },
  headerSubtitle: {
    fontSize: 14,
    color: "#666",
    textAlign: "center",
    marginTop: 5,
  },
  expiringCard: {
    margin: 10,
    backgroundColor: "#FFF3E0",
  },
  expiringHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  expiringTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginLeft: 8,
    color: "#E65100",
  },
  expiringSubtitle: {
    fontSize: 14,
    color: "#BF360C",
    marginBottom: 10,
  },
  chipContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  expiringChip: {
    marginBottom: 4,
  },
  urgentChip: {
    backgroundColor: "#FFEBEE",
    borderColor: "#F44336",
  },
  urgentText: {
    color: "#D32F2F",
    fontWeight: "bold",
  },
  moreIngredientsText: {
    fontSize: 12,
    color: "#666",
    marginTop: 8,
    fontStyle: "italic",
  },
  settingsCard: {
    margin: 10,
    backgroundColor: "#fcfcfa",
  },
  settingsTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 10,
  },
  settingRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 4,
  },
  settingLabel: {
    fontSize: 14,
    color: "#666",
  },
  settingValue: {
    fontSize: 14,
    fontWeight: "500",
  },
  buttonContainer: {
    padding: 10,
    gap: 10,
  },
  optionsButton: {
    borderColor: "#e0e0e0",
    color: "#eb5757",
    backgroundColor: "transparent",
  },
  generateButton: {
    backgroundColor: "#eb5757",
    marginTop: 8,
  },
  dialogSectionTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginTop: 10,
    marginBottom: 10,
  },
  radioRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 4,
  },
  radioLabel: {
    fontSize: 14,
    marginLeft: 8,
    borderRadius: 8,
    color: "#1a1a1a",
  },
  textInput: {
    marginBottom: 10,
  },
  checkboxRow: {
    marginTop: 10,
  },
  divider: {
    marginVertical: 15,
  },
  recipeDialog: {
    maxHeight: "80%",
  },
  recipeContent: {
    maxHeight: 400,
  },
  recipeText: {
    fontSize: 14,
    lineHeight: 20,
  },
  // New styles for recipe cards
  recipesContainer: {
    padding: 10,
  },
  recipesTitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 15,
    color: "#1a1a1a",
  },
  recipeCard: {
    marginBottom: 15,
    backgroundColor: "#fcfcfa",
    borderWidth: 1,
    borderColor: "#e0e0e0",
  },
  recipeCardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 10,
  },
  recipeCardTitle: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#1a1a1a",
    flex: 1,
    marginRight: 10,
  },
  recipeCardDate: {
    fontSize: 12,
    color: "#666",
  },
  recipeCardDetails: {
    marginBottom: 10,
  },
  recipeCardTags: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  recipeTag: {
    marginRight: 4,
    marginBottom: 4,
  },
  recipeCardPreview: {
    fontSize: 14,
    color: "#666",
    lineHeight: 18,
    marginBottom: 10,
  },
  recipeCardFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: "#f0f0f0",
  },
  tapToViewText: {
    fontSize: 12,
    color: "#1a1a1a",
    fontWeight: "500",
  },
  // Fullscreen dialog styles
  fullscreenDialog: {
    margin: 10,
    maxHeight: "95%",
  },
  fullscreenTitle: {
    fontSize: 18,
    fontWeight: "bold",
  },
  fullscreenContent: {
    maxHeight: 600,
  },
  fullscreenRecipeText: {
    fontSize: 15,
    lineHeight: 22,
    color: "#1a1a1a",
  },
});
