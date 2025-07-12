export default function QuestionDisplay({ question, index, total }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <div className="flex justify-between text-sm text-gray-500 mb-2">
        <span>Question {index + 1} of {total}</span>
        <span>Type: {question.type}</span>
      </div>
      <p className="mt-2 text-gray-700 whitespace-pre-line">{question.description}</p>
    </div>
  );
}
