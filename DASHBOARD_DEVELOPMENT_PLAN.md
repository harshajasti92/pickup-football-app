# Dashboard Development Plan - Pickup Football App

## 🎯 Overview
Development roadmap for implementing the main landing page/dashboard with three core sections:
1. **Header Section** - User welcome, quick stats, navigation
2. **Quick Profile Summary Card** - User preferences and profile data display  
3. **Upcoming Games Section** - Game participation and discovery

---

## 🏗️ Phase 1: Foundation Setup

### 1.1 Dashboard Route & Authentication
**New Files to Create:**
```
src/
├── components/dashboard/
│   ├── Dashboard.js
│   ├── Dashboard.css
│   └── index.js
├── contexts/
│   └── AuthContext.js
├── hooks/
│   └── useAuth.js
└── utils/
    └── auth.js
```

**Implementation Tasks:**
- [ ] Create protected dashboard route in App.js
- [ ] Implement authentication context for user state management
- [ ] Add login success redirect to dashboard
- [ ] Create logout functionality
- [ ] Add route protection middleware
- [ ] Implement user session persistence

**Technical Requirements:**
```javascript
// AuthContext structure
const AuthContext = {
  user: {
    id, username, first_name, last_name,
    skill_level, preferred_position, playing_style,
    age_range, bio, is_verified
  },
  login: (userData) => {},
  logout: () => {},
  updateUser: (newData) => {},
  isAuthenticated: boolean
}
```

### 1.2 Database Extensions
**New Tables Required:**
```sql
-- Games table for upcoming games functionality
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(200) NOT NULL,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 90,
    max_players INTEGER DEFAULT 20,
    skill_level_min INTEGER DEFAULT 1,
    skill_level_max INTEGER DEFAULT 10,
    status VARCHAR(20) DEFAULT 'open', -- open, full, cancelled, completed
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game participation tracking
CREATE TABLE game_participants (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'confirmed', -- confirmed, waitlisted, declined
    position_preference VARCHAR(50),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, user_id)
);

-- User availability and preferences
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    preferred_days TEXT[], -- ['monday', 'wednesday', 'friday']
    preferred_times TEXT[], -- ['morning', 'evening']
    max_travel_distance INTEGER DEFAULT 10, -- km
    notifications_enabled BOOLEAN DEFAULT true,
    auto_join_skill_range INTEGER[] DEFAULT '{-2, 2}', -- relative to user skill
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Backend API Extensions:**
- [ ] `/api/games` - CRUD operations for games
- [ ] `/api/games/{id}/join` - Join game endpoint
- [ ] `/api/games/{id}/leave` - Leave game endpoint  
- [ ] `/api/users/{id}/games` - User's games (past, upcoming)
- [ ] `/api/users/{id}/preferences` - User preferences CRUD

---

## 🏠 Phase 2: Header Section Implementation

### 2.1 Component Structure
**Files to Create:**
```
src/components/dashboard/Header/
├── Header.js              # Main header component
├── Header.css             # Header styling
├── UserWelcome.js         # Welcome message with user name
├── QuickStats.js          # Skill level, position, games count
├── UserAvatar.js          # Profile picture or initials
├── NotificationBell.js    # Notifications (future)
├── ProfileDropdown.js     # User menu dropdown
└── index.js               # Export file
```

### 2.2 Header Features & Data

**Welcome Section:**
```javascript
// Dynamic greeting based on time
const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

// Display: "Good morning, Harsha! ⚽"
```

**Quick Stats Display:**
```javascript
// Data pulled from user context and API
const headerStats = {
  skillLevel: user.skill_level,           // from users table
  preferredPosition: user.preferred_position, // from users table  
  gamesPlayed: userStats.games_played,    // calculated from game_participants
  upcomingGames: userStats.upcoming_games // calculated from games
}
```

**Navigation Elements:**
- Profile dropdown (Edit Profile, Settings, Logout)
- Notification bell with badge count
- Mobile hamburger menu
- Search/filter icon (future)

### 2.3 Header Implementation Tasks

**Priority 1 - MVP (Week 2):**
- [x] Basic layout with responsive design
- [x] User greeting with dynamic time awareness
- [x] Display skill level from user data
- [x] Show preferred position with football position icons
- [x] Profile dropdown menu with logout
- [x] Mobile-optimized header collapse

**Priority 2 - Enhanced (Week 3-4):**
- [ ] Games played count (requires games history)
- [ ] Upcoming games quick preview
- [ ] User avatar/profile picture support
- [ ] Notification bell with badge count
- [ ] Search functionality integration

**Design Specifications:**
```css
/* Header styling requirements */
.header {
  height: 70px; /* Desktop */
  height: 60px; /* Mobile */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  /* Stack stats vertically */
  /* Collapse navigation to hamburger */
  /* Reduce padding and font sizes */
}
```

---

## 👤 Phase 3: Quick Profile Summary Card

### 3.1 Component Structure
**Files to Create:**
```
src/components/dashboard/ProfileCard/
├── ProfileCard.js         # Main profile summary card
├── ProfileCard.css        # Card styling and animations
├── SkillMeter.js         # Visual skill level display (1-10)
├── StatsGrid.js          # Grid of user statistics
├── PositionBadge.js      # Position indicator with icon
├── PlayingStyleTag.js    # Style tag component
└── index.js              # Export file
```

### 3.2 Profile Card Data Display

**User Information Layout:**
```javascript
// Profile card data structure
const profileData = {
  // Direct from users table
  basicInfo: {
    name: `${user.first_name} ${user.last_name}`,
    username: user.username,
    skillLevel: user.skill_level,
    preferredPosition: user.preferred_position,
    playingStyle: user.playing_style,
    ageRange: user.age_range,
    bio: user.bio
  },
  
  // Calculated statistics (requires games data)
  statistics: {
    gamesPlayed: 0,      // Count from game_participants
    winRate: 0,          // Calculated from completed games
    goalsScored: 0,      // Future: game_stats table
    assists: 0,          // Future: game_stats table
    averageRating: 0     // Future: player ratings
  }
}
```

**Visual Elements Design:**
- **Position Badge**: Colored badge with football position icon
- **Playing Style Tag**: Styled tag showing Technical/Aggressive/etc
- **Skill Level Meter**: Animated progress bar (1-10 scale)
- **Stats Grid**: 2x2 grid showing key metrics
- **Bio Section**: Expandable text with "Read more" functionality

### 3.3 Profile Card Development Tasks

**Phase 3A - Basic Profile Display (Week 3):**
- [x] Card layout with user photo placeholder
- [x] Display all user preferences from database
- [x] Skill level visual progress bar with animation
- [x] Position badge with football icons
- [x] Playing style tag with color coding
- [x] Age range and bio display
- [x] Responsive card design

**Phase 3B - Enhanced Features (Week 4):**
- [ ] Games played counter (needs games table)
- [ ] Win rate calculation (needs game results tracking)
- [ ] Statistics grid with hover effects
- [ ] Edit profile quick access modal
- [ ] Profile completion percentage
- [ ] Achievement badges display

**Component Specifications:**
```javascript
// SkillMeter component props
<SkillMeter 
  level={7}           // 1-10 scale
  animated={true}     // Animate on load
  showLabel={true}    // Show "7/10" text
  color="#667eea"     // Theme color
/>

// PositionBadge component
<PositionBadge 
  position="Midfielder" 
  icon="midfielder-icon"
  variant="filled"    // filled, outlined, minimal
/>
```

---

## ⚽ Phase 4: Upcoming Games Section

### 4.1 Component Structure
**Files to Create:**
```
src/components/dashboard/GamesSection/
├── GamesSection.js        # Main games container
├── GamesSection.css       # Section styling
├── GameCard.js           # Individual game card
├── GameCard.css          # Game card styling
├── GameStatusBadge.js    # Status indicator (confirmed, waitlisted, etc)
├── PlayerCount.js        # Players count display (15/20)
├── GameActions.js        # Join/Leave/Share buttons
├── EmptyState.js         # No games placeholder
├── LoadingState.js       # Loading skeleton
└── index.js              # Export file
```

### 4.2 Games Data Structure

**Game Object Schema:**
```javascript
// Complete game data structure
const gameData = {
  id: 123,
  title: "Friday Evening Football",
  description: "Casual game for intermediate players",
  location: "Central Park Field A",
  dateTime: "2025-07-26T18:00:00Z",
  duration: 90, // minutes
  maxPlayers: 20,
  skillLevelMin: 5,
  skillLevelMax: 8,
  status: "open", // open, full, cancelled, completed
  
  // Calculated fields
  confirmedPlayers: 18,
  waitlistedPlayers: 3,
  averageSkillLevel: 6.8,
  
  // User's participation status
  userStatus: "confirmed", // confirmed, waitlisted, available, not_joined
  userWaitlistPosition: null,
  
  // Creator info
  createdBy: {
    id: 45,
    name: "John Smith",
    skillLevel: 7
  }
}
```

**Game Participation States:**
- **CONFIRMED** (Green) - User is playing in this game
- **WAITLISTED** (Yellow) - User is on waitlist with position number
- **AVAILABLE** (Blue) - User can join this game
- **FULL** (Gray) - Game is at capacity, cannot join
- **SKILL_MISMATCH** (Orange) - User skill outside game range

### 4.3 Game Card Features

**Information Display:**
```javascript
// Game card layout elements
<GameCard>
  <GameHeader>
    <GameTitle />
    <GameStatusBadge />
  </GameHeader>
  
  <GameDetails>
    <DateTime />        // "Tomorrow, 6:00 PM"
    <Location />        // "Central Park Field A"
    <SkillRange />      // "Skill Level: 5-8"
  </GameDetails>
  
  <ParticipationInfo>
    <PlayerCount />     // "18/20 confirmed"
    <AverageSkill />    // "Avg: 6.8/10"
    <UserStatus />      // "You're confirmed" or "Waitlisted #3"
  </ParticipationInfo>
  
  <GameActions>
    <JoinButton />      // Dynamic based on user status
    <ShareButton />     // Share game details
    <DetailsButton />   // View full game info
  </GameActions>
</GameCard>
```

**Interactive Actions:**
- **Join Game**: Add user to confirmed players
- **Leave Game**: Remove user from game
- **Join Waitlist**: Add user to waitlist queue
- **Leave Waitlist**: Remove from waitlist
- **Share Game**: Copy game link or open share menu
- **View Details**: Navigate to full game details page

### 4.4 Games Section Development Tasks

**Phase 4A - Basic Games Display (Week 4):**
- [ ] Create games database schema
- [ ] Build basic GameCard component with static data
- [ ] Implement games list container
- [ ] Create empty state for no games
- [ ] Add loading states and skeletons
- [ ] Set up games API endpoints (GET /api/games)

**Phase 4B - User Participation (Week 5):**
- [ ] Implement game join/leave functionality
- [ ] Build waitlist management system
- [ ] Add user participation status display
- [ ] Create game filtering by user's skill level
- [ ] Implement real-time player count updates
- [ ] Add game status change handling

**Phase 4C - Enhanced Features (Week 6):**
- [ ] Location-based game discovery
- [ ] Game sharing functionality (copy link, social share)
- [ ] Push notifications for game updates
- [ ] Game recommendations based on user preferences
- [ ] Quick game creation from dashboard
- [ ] Game history integration

**API Endpoints Required:**
```javascript
// Games API specification
GET    /api/games                    // List games (with filters)
POST   /api/games                    // Create new game
GET    /api/games/{id}               // Get game details
PUT    /api/games/{id}               // Update game
DELETE /api/games/{id}               // Delete game

POST   /api/games/{id}/join          // Join game
POST   /api/games/{id}/leave         // Leave game
GET    /api/games/{id}/participants  // Get participants list

GET    /api/users/{id}/games         // User's games (upcoming, past)
GET    /api/users/{id}/games/stats   // User's game statistics
```

---

## 🚀 Implementation Timeline

### **Week 1: Foundation Setup**
**Phase 1 Complete**
- [ ] Dashboard routing and authentication context
- [ ] User session management and persistence
- [ ] Basic database schema extensions
- [ ] Backend API structure setup

**Deliverable:** Authenticated dashboard route with user context

### **Week 2: Header Implementation**
**Phase 2A Complete**
- [ ] Header component with user welcome
- [ ] Quick stats display (skill, position)
- [ ] Profile dropdown with logout
- [ ] Responsive mobile design

**Deliverable:** Fully functional header section

### **Week 3: Profile Card**
**Phase 3A Complete**
- [ ] Profile summary card with all user data
- [ ] Skill level visualization
- [ ] Position and style badges
- [ ] Responsive card layout

**Deliverable:** Complete profile summary display

### **Week 4: Games Foundation**
**Phase 4A Complete**
- [ ] Games database schema and API
- [ ] Basic game cards display
- [ ] Empty states and loading states
- [ ] Games section layout

**Deliverable:** Games section with static data

### **Week 5: Games Functionality**
**Phase 4B Complete**
- [ ] Game join/leave functionality
- [ ] Waitlist management
- [ ] User participation status
- [ ] Real-time updates

**Deliverable:** Interactive games participation

### **Week 6: Polish & Enhancement**
**Phase 4C Complete**
- [ ] Game filtering and recommendations
- [ ] Sharing functionality
- [ ] Performance optimizations
- [ ] Mobile UX enhancements

**Deliverable:** Production-ready dashboard

---

## 🎯 MVP Definition

### **Minimal Viable Dashboard (Week 3)**
**What users will see:**
- ✅ Header with personalized welcome and basic stats
- ✅ Profile card showing all their preferences and information
- ✅ "No upcoming games" empty state with clear call-to-action
- ✅ Fully responsive mobile-first design
- ✅ Smooth navigation and logout functionality

### **Complete Dashboard Experience (Week 6)**
**Full functionality:**
- ✅ All sections populated with real data
- ✅ Interactive game participation (join/leave/waitlist)
- ✅ Real-time updates and notifications
- ✅ Game discovery and filtering
- ✅ Integration ready for team balancing algorithm
- ✅ Optimized performance and mobile experience

---

## 📱 Mobile-First Design Considerations

### **Responsive Breakpoints:**
```css
/* Mobile First Approach */
.dashboard {
  /* Base styles for mobile (320px+) */
}

@media (min-width: 768px) {
  /* Tablet styles */
}

@media (min-width: 1024px) {
  /* Desktop styles */
}
```

### **Touch Interactions:**
- **Swipe Actions**: Swipe game cards to join/leave
- **Pull to Refresh**: Refresh games list
- **Tap Targets**: Minimum 44px touch targets
- **Haptic Feedback**: Confirm actions with vibration

### **Performance Optimizations:**
- **Lazy Loading**: Load game cards as user scrolls
- **Image Optimization**: Responsive images with proper sizing
- **Code Splitting**: Load dashboard components on demand
- **Caching**: Cache user data and recent games

---

## 🔧 Technical Architecture

### **State Management:**
```javascript
// Dashboard state structure
const dashboardState = {
  user: AuthContext.user,
  games: {
    upcoming: [],
    userGames: [],
    loading: false,
    error: null
  },
  ui: {
    selectedFilter: 'all',
    showMobileMenu: false,
    notifications: []
  }
}
```

### **Component Hierarchy:**
```
Dashboard
├── Header
│   ├── UserWelcome
│   ├── QuickStats
│   └── ProfileDropdown
├── ProfileCard
│   ├── SkillMeter
│   ├── StatsGrid
│   └── PositionBadge
└── GamesSection
    ├── GameCard[]
    ├── EmptyState
    └── LoadingState
```

### **Data Flow:**
1. **Authentication**: Login → Store user in context → Redirect to dashboard
2. **Dashboard Load**: Fetch user games → Display in sections → Enable interactions
3. **Game Actions**: User interaction → API call → Update local state → Re-render
4. **Real-time**: WebSocket connection → Receive updates → Update game states

---

## 📋 Testing Strategy

### **Unit Testing:**
- [ ] Individual component functionality
- [ ] User context and auth hooks
- [ ] Game state management
- [ ] API integration functions

### **Integration Testing:**
- [ ] Authentication flow end-to-end
- [ ] Game join/leave workflow
- [ ] Dashboard data loading
- [ ] Mobile responsive behavior

### **User Testing:**
- [ ] Dashboard navigation and usability
- [ ] Mobile touch interactions
- [ ] Game discovery and joining flow
- [ ] Profile information display

---

*This development plan serves as the blueprint for implementing the Pickup Football dashboard. Each phase builds upon the previous one, ensuring a solid foundation while delivering user value incrementally.*

**Next Steps:** Begin with Phase 1 implementation - setting up the dashboard foundation and authentication context.
