"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema, FormValues } from "@/lib/formSchema";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

// Helper function for rendering radio groups
const RadioGroupField = ({
  name,
  label,
  options,
  setValue,
  errors,
  idPrefix = "",
}) => {
  const prefix = idPrefix ? `${idPrefix}-` : "";

  return (
    <div>
      <Label className="block mb-2 text-base font-medium">{label}</Label>
      <RadioGroup onValueChange={(val) => setValue(name, val)}>
        {options.map(([val, label]) => (
          <div key={val} className="flex items-center space-x-2">
            <RadioGroupItem value={val} id={`${prefix}${val}`} />
            <Label htmlFor={`${prefix}${val}`}>{label}</Label>
          </div>
        ))}
      </RadioGroup>
      {errors[name] && <p className="text-red-500">{errors[name].message}</p>}
    </div>
  );
};

export default function Home() {
  const [message, setMessage] = useState("");
  const router = useRouter();

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: FormValues) => {
    try {
      console.log("Form Data:", data);

      const response = await fetch("http://127.0.0.1:8000/api/v1/predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to get prediction");
      }

      const result = await response.json(); // assuming { result: number }
      router.push(`/result/${result.result}`);
    } catch (error) {
      console.error("Submission error:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error("Error:", err));
  }, []);

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-xl mx-auto p-8 space-y-8"
    >
      {/* Gender */}
      <RadioGroupField
        name="gender"
        label="Gender"
        options={[
          ["male", "Male"],
          ["female", "Female"],
          ["other", "Other"],
        ]}
        setValue={setValue}
        errors={errors}
      />

      {/* Age */}
      <div>
        <Label htmlFor="age" className="block mb-2 text-base font-medium">
          Age
        </Label>
        <Input
          id="age"
          type="number"
          min="0"
          step="1"
          {...register("age", { valueAsNumber: true })}
        />
        {errors.age && <p className="text-red-500">{errors.age.message}</p>}
      </div>

      {/* Height */}
      <div>
        <Label htmlFor="height" className="block mb-2 text-base font-medium">
          Height (cm)
        </Label>
        <Input
          id="height"
          type="number"
          min="0"
          step="1"
          {...register("height", { valueAsNumber: true })}
        />
        {errors.height && (
          <p className="text-red-500">{errors.height.message}</p>
        )}
      </div>

      {/* Weight */}
      <div>
        <Label htmlFor="weight" className="block mb-2 text-base font-medium">
          Weight (kg)
        </Label>
        <Input
          id="weight"
          type="number"
          min="0"
          step="0.1"
          {...register("weight", { valueAsNumber: true })}
        />
        {errors.weight && (
          <p className="text-red-500">{errors.weight.message}</p>
        )}
      </div>

      {/* Hydration */}
      <RadioGroupField
        name="hydration"
        label="Hydration"
        options={[
          ["poor", "Poor (rarely drink water)"],
          ["moderate", "Moderate (1–2 liters/day)"],
          ["good", "Good (2–3 liters/day)"],
          ["excellent", "Excellent (3+ liters/day)"],
        ]}
        setValue={setValue}
        errors={errors}
      />

      {/* Physical Activity */}
      <RadioGroupField
        name="activity"
        label="Activity Level"
        options={[
          ["low", "Low (mostly sedentary)"],
          ["moderate", "Moderate (exercise few days/week)"],
          ["high", "High (exercise 5+ days/week or physical job)"],
        ]}
        setValue={setValue}
        errors={errors}
      />

      {/* Medication */}
      <RadioGroupField
        name="medication"
        label="Medications"
        options={[
          ["yes", "Yes"],
          ["no", "No"],
        ]}
        setValue={setValue}
        errors={errors}
      />

      {/* Fiber Intake */}
      <RadioGroupField
        name="fibers"
        label="Dietary Fiber"
        options={[
          ["not much", "Not much"],
          ["moderate", "Moderate"],
          ["a lot", "A lot"],
        ]}
        setValue={setValue}
        errors={errors}
      />

      {/* Fat Intake */}
      <RadioGroupField
        name="fatIntake"
        label="Fat Intake"
        options={[
          ["not much", "Not much"],
          ["moderate", "Moderate"],
          ["a lot", "A lot"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="fat"
      />

      {/* Spice Level */}
      <RadioGroupField
        name="spiceLevel"
        label="Spice Level"
        options={[
          ["not spicy", "Not spicy"],
          ["moderate", "Moderate"],
          ["spicy", "Spicy"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="spice"
      />

      {/* Greasy Meals Per Week */}
      <RadioGroupField
        name="greasyMealsPerWeek"
        label="Greasy/Fried Meals Per Week"
        options={[
          ["0-2", "0-2"],
          ["3-4", "3-4"],
          ["5 and more", "5 and more"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="greasy"
      />

      {/* Dairy Intake */}
      <RadioGroupField
        name="dairyIntake"
        label="Dairy Consumption"
        options={[
          ["yes", "Yes"],
          ["no", "No"],
          ["occasionally", "Occasionally"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="dairy"
      />

      {/* Processed Food Per Day */}
      <RadioGroupField
        name="processedFoodPerDay"
        label="Processed Food Servings Per Day"
        options={[
          ["0-2", "0-2"],
          ["3-4", "3-4"],
          ["5 and more", "5 and more"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="processed"
      />

      {/* Fruits & Vegetables Per Day */}
      <RadioGroupField
        name="fruitsVeggiesPerDay"
        label="Fruits & Vegetables Servings Per Day"
        options={[
          ["0-2", "0-2"],
          ["3-4", "3-4"],
          ["5 and more", "5 and more"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="fruits"
      />

      {/* Wiping Method */}
      <RadioGroupField
        name="wipingMethod"
        label="Wiping Method"
        options={[
          ["1-ply paper", "1-ply paper"],
          ["2-ply paper", "2-ply paper"],
          ["3-ply paper", "3-ply paper"],
          ["wet wipes", "Wet wipes"],
          ["bidet/water", "Bidet/water"],
          ["other", "Other"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="wipe"
      />

      {/* Stool Consistency */}
      <RadioGroupField
        name="stoolConsistency"
        label="Stool Consistency"
        options={[
          ["hard and lumpy", "Hard and lumpy"],
          ["firm and smooth", "Firm and smooth"],
          ["soft", "Soft"],
          ["sticky or mushy", "Sticky or mushy"],
          ["watery", "Watery"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="consistency"
      />

      {/* Stool Color */}
      <RadioGroupField
        name="stoolColor"
        label="Stool Color"
        options={[
          ["brown", "Brown"],
          ["yellow", "Yellow"],
          ["green", "Green"],
          ["black", "Black"],
          ["red or bloody", "Red or bloody"],
          ["other", "Other"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="color"
      />

      {/* Stool Smell Intensity */}
      <RadioGroupField
        name="stoolSmellIntensity"
        label="Stool Smell Intensity"
        options={[
          ["1", "1"],
          ["2", "2"],
          ["3", "3"],
          ["4", "4"],
          ["5", "5"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="smell"
      />

      {/* Bowel Movements Per Week */}
      <div>
        <Label
          htmlFor="bowelMovementsPerWeek"
          className="block mb-2 text-base font-medium"
        >
          Bowel Movements Per Week
        </Label>
        <Input
          id="bowelMovementsPerWeek"
          type="number"
          min="0"
          step="1"
          {...register("bowelMovementsPerWeek", { valueAsNumber: true })}
        />
        {errors.bowelMovementsPerWeek && (
          <p className="text-red-500">{errors.bowelMovementsPerWeek.message}</p>
        )}
      </div>

      {/* Caffeine Per Day */}
      <RadioGroupField
        name="caffeinePerDay"
        label="Caffeinated Beverages Per Day"
        options={[
          ["0-2", "0-2"],
          ["3-5", "3-5"],
          ["5 and more", "5 and more"],
        ]}
        setValue={setValue}
        errors={errors}
        idPrefix="caffeine"
      />

      {/* Sleep Hours */}
      <div>
        <Label
          htmlFor="sleepHours"
          className="block mb-2 text-base font-medium"
        >
          Hours of Sleep Per Night
        </Label>
        <Input
          id="sleepHours"
          type="number"
          min="1"
          max="24"
          step="1"
          {...register("sleepHours", { valueAsNumber: true })}
        />
        {errors.sleepHours && (
          <p className="text-red-500">{errors.sleepHours.message}</p>
        )}
      </div>

      {/* Submit */}
      <div>
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </div>
    </form>
  );
}
