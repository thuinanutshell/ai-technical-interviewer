'use client';

import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';
import { useState } from 'react';
import Editor from 'react-simple-code-editor';

export default function CodeEditor({ language = 'python', initialCode = '' }) {
  const [code, setCode] = useState(initialCode);

  const highlight = (code) => Prism.highlight(code, Prism.languages[language], language);

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden">
      <Editor
        value={code}
        onValueChange={setCode}
        highlight={highlight}
        padding={12}
        className="font-mono text-sm bg-white"
        style={{ minHeight: '200px', fontFamily: 'monospace' }}
      />
    </div>
  );
}
