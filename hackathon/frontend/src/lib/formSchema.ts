import { z } from "zod";

export const formSchema = z.object({
  gender: z.enum(["male", "female", "other"]),
  age: z
    .number({ invalid_type_error: "Please enter a valid age" })
    .min(13, "Age must be at least 13 years old"),
  height_cm: z
    .number({ invalid_type_error: "Please enter a valid height" })
    .min(50, "Height must be at least 50cm"),
  weight_kg: z
    .number({ invalid_type_error: "Please enter a valid weight" })
    .min(10, "Weight must be at least 10kg"),
  hydration_level: z.enum(["poor", "moderate", "good", "excellent"]),
  activity_level: z.enum(["low", "moderate", "high"]),
  meds_affecting_gut: z.enum(["yes", "no"]),
  fiber_grams: z.enum(["not much", "moderate", "a lot"]),

  fat_grams: z.enum(["not much", "moderate", "a lot"]),
  spiciness: z.enum(["not spicy", "moderate", "spicy"]),
  weekly_greasy_meals: z.enum(["0-2", "3-4", "5 and more"]),
  dairy_freq: z.enum(["yes", "no", "occasionally"]),
  processed_servings: z.enum(["0-2", "3-4", "5 and more"]),
  fv_servings: z.enum(["0-2", "3-4", "5 and more"]),
  toilet_method: z.enum([
    "1-ply paper",
    "2-ply paper",
    "3-ply paper",
    "wet wipes",
    "bidet/water",
    "other",
  ]),
  stool_consistency: z.enum([
    "hard and lumpy",
    "firm and smooth",
    "soft",
    "sticky or mushy",
    "watery",
  ]),
  stool_color: z.enum([
    "brown",
    "yellow",
    "green",
    "black",
    "red or bloody",
    "other",
  ]),
  smell_intensity: z.enum(["1", "2", "3", "4", "5"]),
  weekly_bms: z
    .number({ invalid_type_error: "Please enter a valid number" })
    .min(0),
  caffeinated_beverages_per_day: z.enum(["0-2", "3-5", "5 and more"]),
  sleep_hours: z
    .number({ invalid_type_error: "Please enter a valid number of hours" })
    .min(1)
    .max(24),
});

export type FormValues = z.infer<typeof formSchema>;
