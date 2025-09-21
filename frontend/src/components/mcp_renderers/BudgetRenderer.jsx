import React from "react";

const BudgetRenderer = ({ data }) => {
  const budget = data?.budget || data?.data?.budget;
  const summary = data?.summary || data?.data?.summary;

  if (!budget) {
    return <p className="text-gray-500">No budget data available.</p>;
  }

  return (
    <div className="p-4 bg-indigo-50 rounded-lg shadow-sm">
      <p className="text-gray-600 font-medium">
        {summary || "Here is the budget breakdown."}
      </p>
      <div className="mt-2">
        <p className="font-semibold text-indigo-700">
          Total Estimated Cost: ₹{budget.totalEstimatedCost}
        </p>
        <ul className="list-disc list-inside mt-2">
          {budget.categories?.map((category, index) => (
            <li key={index} className="text-gray-800">
              {category.name}: ₹{category.amount}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default BudgetRenderer;
