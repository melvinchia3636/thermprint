import { useCalendarPrinting } from "../context/CalendarPrintingContext";
import SelectField from "../../../components/ui/SelectField";
import StepCard from "../../../components/ui/StepCard";

const MONTHS = [
  { value: 1, label: "January" },
  { value: 2, label: "February" },
  { value: 3, label: "March" },
  { value: 4, label: "April" },
  { value: 5, label: "May" },
  { value: 6, label: "June" },
  { value: 7, label: "July" },
  { value: 8, label: "August" },
  { value: 9, label: "September" },
  { value: 10, label: "October" },
  { value: 11, label: "November" },
  { value: 12, label: "December" },
];

export default function CalendarConfigStep() {
  const { form, setForm, setStep } = useCalendarPrinting();

  return (
    <StepCard
      title="Calendar"
      icon="tabler:calendar"
      onNext={() => setStep(1)}
      nextDisabled={!form.year || !form.month}
      nextLabel="Preview"
    >
      <label className="flex flex-col gap-1.5 px-3 rounded-box bg-base-300/50">
        <span className="text-sm font-medium text-base-content truncate">
          Year
        </span>
        <input
          id="cal-year"
          type="number"
          min={2000}
          max={2100}
          value={form.year}
          onChange={(e) =>
            setForm({
              year: Number(e.target.value) || new Date().getFullYear(),
            })
          }
          className="input input-bordered w-full"
        />
      </label>
      <div className="mt-4">
        <SelectField
          label="Month"
          value={form.month}
          options={MONTHS}
          onChange={(v) => setForm({ month: v })}
        />
      </div>
    </StepCard>
  );
}
