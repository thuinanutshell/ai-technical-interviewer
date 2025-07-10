"use client"

import { useRouter } from 'next/navigation';
import { createContext, useEffect, useState, useContext } from 'react';
import { authAPI, clearAuthToken, getAuthToken, setAuthToken } from '../lib/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter()

    useEffect(() => {
        const token = getAuthToken();
        if (token) {
            setUser({ token });
        }
        setLoading(false);
    }, []);

    const login = async (credentials) => {
        try {
            setLoading(true);
            const response = await authAPI.login(credentials);

            setAuthToken(response.access_token);
            setUser({ token: response.access_token });

            router.push('/dashboard');
            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || "Login failed"
            };
        } finally {
            setLoading(false)
        }
    };

    const register = async (userData) => {
        try {
            setLoading(true);
            const response = await authAPI.register(userData);

            // Auto-login after registration
            const loginResult = await login({
                email: userData.email,
                password: userData.password,
            });

            return loginResult;
        } catch (error) {
            setLoading(false);
            return {
                success: false,
                error: error.response?.data?.detail || 'Registration failed'
            };
        }
    };

    const logout = async () => {
        try {
            await authAPI.logout();
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            clearAuthToken();
            setUser(null);
            router.push('/auth/login');
        }
    };

    const value = {
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
    };

    return (
        <AuthContext.Provider value={value}>
        {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};