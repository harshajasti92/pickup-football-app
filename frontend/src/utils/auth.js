// Authentication utility functions

export const isTokenValid = (token) => {
  if (!token) return false;
  
  try {
    // For now, we'll just check if token exists
    // In the future, you can add JWT token validation here
    return true;
  } catch (error) {
    return false;
  }
};

export const getStoredUser = () => {
  try {
    const userData = localStorage.getItem('userData');
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error('Error parsing stored user data:', error);
    return null;
  }
};

export const clearStoredUser = () => {
  localStorage.removeItem('userData');
};

export const storeUser = (userData) => {
  localStorage.setItem('userData', JSON.stringify(userData));
};

// Format user display name
export const getUserDisplayName = (user) => {
  if (!user) return '';
  return `${user.first_name} ${user.last_name}`;
};

// Get user initials for avatar
export const getUserInitials = (user) => {
  if (!user) return 'U';
  const firstInitial = user.first_name ? user.first_name.charAt(0).toUpperCase() : '';
  const lastInitial = user.last_name ? user.last_name.charAt(0).toUpperCase() : '';
  return `${firstInitial}${lastInitial}` || 'U';
};

// Check if user profile is complete
export const isProfileComplete = (user) => {
  if (!user) return false;
  
  const requiredFields = [
    'username', 'first_name', 'last_name', 
    'skill_level', 'preferred_position', 'playing_style'
  ];
  
  return requiredFields.every(field => user[field] !== null && user[field] !== undefined && user[field] !== '');
};
