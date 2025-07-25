import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './SignupForm.css';

const SignupForm = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    ageRange: '',
    bio: '',
    skillLevel: 5,
    preferredPosition: '',
    playingStyle: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Predefined options based on database constraints
  const ageRangeOptions = ['18-25', '26-35', '36-45', '46+'];
  const positionOptions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any'];
  const playingStyleOptions = ['Aggressive', 'Technical', 'Physical', 'Balanced', 'Creative', 'Defensive'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required field validations
    if (!formData.username.trim()) newErrors.username = 'Username is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (!formData.confirmPassword) newErrors.confirmPassword = 'Please confirm your password';
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';

    // Password validation
    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Username validation (no spaces, reasonable length)
    if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters long';
    }
    if (formData.username.includes(' ')) {
      newErrors.username = 'Username cannot contain spaces';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Prepare data for API
      const userData = {
        username: formData.username,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        age_range: formData.ageRange || null,
        bio: formData.bio || null,
        skill_level: parseInt(formData.skillLevel),
        preferred_position: formData.preferredPosition || null,
        playing_style: formData.playingStyle || null
      };

      // Send data to FastAPI backend
      const response = await fetch('http://localhost:8000/api/users/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
      }

      const newUser = await response.json();
      console.log('User created successfully:', newUser);
      
      alert(`Signup successful! Welcome to Pickup Football, ${newUser.first_name}! You can now log in with your credentials.`);
      
      // Reset form
      setFormData({
        username: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
        ageRange: '',
        bio: '',
        skillLevel: 5,
        preferredPosition: '',
        playingStyle: ''
      });

      // Redirect to login page after successful signup
      navigate('/login');

    } catch (error) {
      console.error('Signup error:', error);
      alert(`Signup failed: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-form">
        <h2>Join Pickup Football</h2>
        <p className="signup-subtitle">Create your player profile</p>
        
        <form onSubmit={handleSubmit}>
          {/* Basic Information */}
          <div className="form-section">
            <h3>Basic Information</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name *</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  className={errors.firstName ? 'error' : ''}
                  placeholder="Enter your first name"
                />
                {errors.firstName && <span className="error-message">{errors.firstName}</span>}
              </div>
              
              <div className="form-group">
                <label htmlFor="lastName">Last Name *</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  className={errors.lastName ? 'error' : ''}
                  placeholder="Enter your last name"
                />
                {errors.lastName && <span className="error-message">{errors.lastName}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="username">Username *</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                className={errors.username ? 'error' : ''}
                placeholder="Choose a unique username"
              />
              {errors.username && <span className="error-message">{errors.username}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="password">Password *</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  placeholder="At least 8 characters"
                />
                {errors.password && <span className="error-message">{errors.password}</span>}
              </div>
              
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password *</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={errors.confirmPassword ? 'error' : ''}
                  placeholder="Confirm your password"
                />
                {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="ageRange">Age Range</label>
              <select
                id="ageRange"
                name="ageRange"
                value={formData.ageRange}
                onChange={handleChange}
              >
                <option value="">Select age range</option>
                {ageRangeOptions.map(range => (
                  <option key={range} value={range}>{range}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Player Information */}
          <div className="form-section">
            <h3>Player Profile</h3>
            
            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                placeholder="Tell us about yourself and your playing experience..."
                rows="3"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="skillLevel">
                  Skill Level: {formData.skillLevel}/10
                </label>
                <input
                  type="range"
                  id="skillLevel"
                  name="skillLevel"
                  min="1"
                  max="10"
                  value={formData.skillLevel}
                  onChange={handleChange}
                  className="skill-slider"
                />
                <div className="skill-labels">
                  <span>Beginner</span>
                  <span>Professional</span>
                </div>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="preferredPosition">Preferred Position</label>
                <select
                  id="preferredPosition"
                  name="preferredPosition"
                  value={formData.preferredPosition}
                  onChange={handleChange}
                >
                  <option value="">Select position</option>
                  {positionOptions.map(position => (
                    <option key={position} value={position}>{position}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="playingStyle">Playing Style</label>
                <select
                  id="playingStyle"
                  name="playingStyle"
                  value={formData.playingStyle}
                  onChange={handleChange}
                >
                  <option value="">Select style</option>
                  {playingStyleOptions.map(style => (
                    <option key={style} value={style}>{style}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            className="submit-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="form-footer">
          <p>Already have an account? <Link 
              to="/login" 
              className="login-link"
            >
              Sign in here
            </Link></p>
        </div>
      </div>
    </div>
  );
};

export default SignupForm;
