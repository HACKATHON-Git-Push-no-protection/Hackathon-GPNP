import { z } from "zod";

export const formSchema = z.object({
  gender: z.enum(["male", "female", "other"]),
  age: z.number({ invalid_type_error: "Please enter a valid age" }).min(13, "Age must be at least 13 years old"),
  height: z.number({ invalid_type_error: "Please enter a valid height" }).min(50, "Height must be at least 50cm"),
  weight: z.number({ invalid_type_error: "Please enter a valid weight" }).min(10, "Weight must be at least 10kg"),
  hydration: z.enum(["poor", "moderate", "good", "excellent"]),
  activity: z.enum(["low", "moderate", "high"]),
  medication: z.enum(["yes", "no"]),
  fibers: z.enum(["not much", "moderate", "a lot"]),

  fatIntake: z.enum(["not much", "moderate", "a lot"]),
  spiceLevel: z.enum(["not spicy", "moderate", "spicy"]),
  greasyMealsPerWeek: z.enum(["0-2", "3-4", "5 and more"]),
  dairyIntake: z.enum(["yes", "no", "occasionally"]),
  processedFoodPerDay: z.enum(["0-2", "3-4", "5 and more"]),
  fruitsVeggiesPerDay: z.enum(["0-2", "3-4", "5 and more"]),
  wipingMethod: z.enum([
    "1-ply paper",
    "2-ply paper",
    "3-ply paper",
    "wet wipes",
    "bidet/water",
    "other",
  ]),
  stoolConsistency: z.enum([
    "hard and lumpy",
    "firm and smooth",
    "soft",
    "sticky or mushy",
    "watery",
  ]),
  stoolColor: z.enum([
    "brown",
    "yellow",
    "green",
    "black",
    "red or bloody",
    "other",
  ]),
  stoolSmellIntensity: z.enum([
    "1",
    "2",
    "3",
    "4",
    "5"]),
  bowelMovementsPerWeek: z
    .number({ invalid_type_error: "Please enter a valid number" })
    .min(0),
  caffeinePerDay: z.enum(["0-2", "3-5", "5 and more"]),
  sleepHours: z
    .number({ invalid_type_error: "Please enter a valid number of hours" })
    .min(1)
    .max(24),
});

export type FormValues = z.infer<typeof formSchema>;
