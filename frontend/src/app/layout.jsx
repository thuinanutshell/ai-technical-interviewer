import { AuthProvider } from '../hooks/useAuth';
import './globals.css';

export const metadata = {
  title: 'AI Technical Interviewer',
  description: 'Practice technical interviews with AI',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}