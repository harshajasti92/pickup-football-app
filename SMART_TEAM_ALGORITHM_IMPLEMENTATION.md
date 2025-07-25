# Smart Team Algorithm - Implementation Guide

## 🚀 **Quick Start Implementation**

This guide provides the conceptual structure and design patterns needed to implement the smart team balancing algorithm in your Pickup Football app.

---

## 📁 **File Structure to Create**

**Backend Structure:**
- **algorithms/** - Core algorithm modules
  - **team_balancer.py** - Core algorithm logic
  - **balance_calculator.py** - Balance scoring functions
  - **position_optimizer.py** - Position distribution logic
  - **utils.py** - Helper functions

**Database:**
- **05_create_team_assignments_table.sql** - New database table

**Frontend Structure:**
- **components/teams/** - Team generation components
  - **TeamGenerator.js** - Main team generation UI
  - **TeamDisplay.js** - Show generated teams
  - **BalanceScore.js** - Balance metrics display
  - **TeamGenerator.css** - Styling

---

## 🗄️ **1. Database Schema Implementation**

### **Create Team Assignments Table**
**Database Schema for Team Balancing:**

**Table: team_assignments**
- **id** - Primary key
- **game_id** - Reference to games table
- **user_id** - Reference to users table  
- **team_name** - 'Team A' or 'Team B'
- **assigned_position** - Player's assigned position
- **balance_score** - Algorithm confidence score (0-100)
- **algorithm_version** - Version tracking
- **created_at/updated_at** - Timestamps
- **Unique constraint** - One assignment per user per game

**Indexes:**
- game_id for fast game lookups
- team_name for team-based queries

---

## 🧠 **2. Core Algorithm Implementation**

### **Main Team Balancer (backend/app/algorithms/team_balancer.py)**
**Core Algorithm Class Structure:**

**Player Data Class:**
- Store player attributes: id, username, names, skill_level
- Include position preferences and playing style
- Track age range for balance calculations

**TeamBalancer Class:**
- Initialize with balance weights and calculators
- Main method: generate_balanced_teams()
- Return team assignments with balance score

**Algorithm Flow:**
1. **Pre-process players** - Sort and organize by skill/position
2. **Snake draft distribution** - Alternate high-skill players
3. **Position optimization** - Ensure proper formation coverage
4. **Final balance optimization** - Strategic swaps for improvement

### **Balance Calculator (backend/app/algorithms/balance_calculator.py)**
**Balance Scoring System:**

**BalanceCalculator Class:**
- Calculate skill balance between teams (40% weight)
- Evaluate position distribution adequacy (25% weight)
- Assess playing style compatibility (15% weight)
- Factor in age distribution balance (10% weight)
- Consider team size equality (10% weight)

**Scoring Methods:**
- **calculate_total_balance()** - Main scoring function
- **calculate_skill_balance()** - Average skill difference
- **calculate_position_balance()** - Formation requirements
- **calculate_style_balance()** - Team chemistry
- **calculate_age_balance()** - Age distribution

**Style Compatibility Matrix:**
- Define complementary playing style pairings
- Identify potential style clashes
- Balance diversity with compatibility

---

## 🎯 **3. Backend API Implementation**

### **New API Endpoints**

**Team Generation Endpoints:**
- **POST /api/games/{game_id}/generate-teams**
  - Verify user is game creator
  - Get confirmed players for the game
  - Convert to Player objects
  - Run team balancing algorithm
  - Save assignments to database
  - Return team assignments with balance score

- **GET /api/games/{game_id}/teams**
  - Retrieve current team assignments
  - Organize by Team A and Team B
  - Include player details and balance score

**Authentication & Permissions:**
- Only game creators can generate teams
- Minimum 4 confirmed players required
- Validate game status is 'open'

**Database Operations:**
- Clear existing team assignments before generating new ones
- Store team assignments with balance scores
- Track algorithm version for future improvements

---

## 🎨 **4. Frontend Implementation**

### **Team Generator Component (frontend/src/components/teams/TeamGenerator.js)**
**Main Team Generation Interface:**

**Component Features:**
- Display team generation button for game creators
- Show player count requirements
- Handle team generation API calls
- Display loading states during generation
- Show error messages for failures

**User Experience Flow:**
1. Check if user can generate teams (creator + minimum players)
2. Display generation button with player count
3. Show loading state during API call
4. Display generated teams with balance score
5. Provide shuffle/regenerate option

### **Team Display Component (frontend/src/components/teams/TeamDisplay.js)**
**Team Visualization:**

**Display Features:**
- Side-by-side team layout (Team A vs Team B)
- Player cards with skill levels and positions
- Team statistics (average skill, player count)
- Position icons and skill color coding
- Responsive design for mobile devices

**Player Card Information:**
- Player name and username
- Skill level with color coding
- Assigned position with icons
- Visual skill indicators

### **Balance Score Component (frontend/src/components/teams/BalanceScore.js)**
**Balance Metrics Display:**

**Score Visualization:**
- Overall balance score (0-100)
- Color-coded score ranges (excellent, good, fair, poor)
- Breakdown by balance factors
- Progress bars for each metric
- Skill difference indicator

**Balance Factors Shown:**
- Skill Balance percentage
- Position Balance percentage  
- Style Balance percentage
- Team size and fairness metrics

---

## 🎨 **5. CSS Styling Approach**

### **Design System**
**Color Scheme:**
- Team A: Blue theme (#667eea)
- Team B: Purple theme (#764ba2)
- Success: Green for excellent balance
- Warning: Orange for fair balance
- Error: Red for poor balance

**Layout Patterns:**
- Card-based design with shadows
- Responsive grid system
- Mobile-first approach
- Consistent spacing and typography

**Component Styling:**
- **Team Generator**: Prominent action buttons
- **Team Display**: Side-by-side team cards
- **Balance Score**: Progress bars and metrics
- **Player Cards**: Skill badges and position icons

---

## 🚀 **6. Integration Steps**

### **Step 1: Database Setup**
- Create team_assignments table
- Add indexes for performance
- Test table creation and constraints

### **Step 2: Backend Implementation**
- Create algorithm modules in backend/app/algorithms/
- Implement core balancing logic
- Add API endpoints to main.py
- Test algorithm with sample data

### **Step 3: Frontend Integration**
- Create team components in frontend/src/components/teams/
- Add team generation to game management interface
- Implement balance score visualization
- Test responsive design

### **Step 4: Testing & Validation**
- Unit test algorithm components
- Integration test API endpoints
- User acceptance testing
- Performance optimization

---

## 🧪 **7. Testing Strategy**

### **Algorithm Testing**
**Unit Tests:**
- Test skill balance within acceptable ranges
- Verify position requirements are met
- Test edge cases (odd numbers, missing positions)
- Performance testing with various player counts

**Integration Tests:**
- End-to-end team generation workflow
- Database persistence validation
- API response accuracy
- Frontend team display correctness

### **User Testing**
**Usability Tests:**
- Team generation workflow
- Balance score interpretation
- Mobile device functionality
- Error handling and recovery

---

## 📈 **8. Success Metrics & Monitoring**

### **Technical Metrics**
- **Balance Score Average**: Target >85/100
- **Generation Time**: Target <2 seconds
- **Position Coverage**: Target >95% proper distribution
- **Algorithm Accuracy**: Compare against manual team creation

### **User Experience Metrics**
- **Adoption Rate**: Percentage of games using auto-generation
- **User Satisfaction**: Rating on team fairness
- **Manual Override Rate**: How often users modify teams
- **Game Completion Rate**: Impact on game completion

---

## 💡 **9. Future Enhancements**

### **Version 1.1 Improvements**
- Manual player swap functionality
- Algorithm parameter tuning
- Historical performance integration
- Advanced position versatility

### **Version 2.0 Advanced Features**
- Machine learning optimization
- Player chemistry factors
- Tournament mode balancing
- Predictive balance modeling

---

## 🎯 **Implementation Priority**

### **Week 1: Core Algorithm**
- Database schema creation
- Basic balancing algorithm implementation
- Unit testing framework

### **Week 2: API Integration** 
- Backend endpoint implementation
- Database integration
- API testing and validation

### **Week 3: Frontend Components**
- Team generation UI
- Team display components
- Balance score visualization

### **Week 4: Testing & Polish**
- Integration testing
- User experience refinement
- Performance optimization
- Documentation completion

---

**This implementation guide provides the conceptual framework and architectural approach needed to build a sophisticated team balancing system while maintaining code-free documentation for strategic planning purposes.**

---

## 📁 **File Structure to Create**

**Backend Structure:**
- **algorithms/** - Core algorithm modules
  - **team_balancer.py** - Core algorithm logic
  - **balance_calculator.py** - Balance scoring functions
  - **position_optimizer.py** - Position distribution logic
  - **utils.py** - Helper functions

**Database:**
- **05_create_team_assignments_table.sql** - New database table

**Frontend Structure:**
- **components/teams/** - Team generation components
  - **TeamGenerator.js** - Main team generation UI
  - **TeamDisplay.js** - Show generated teams
  - **BalanceScore.js** - Balance metrics display
  - **TeamGenerator.css** - Styling

---

## 🗄️ **1. Database Schema Implementation**

### **Create Team Assignments Table**
**Database Schema for Team Balancing:**

**Table: team_assignments**
- **id** - Primary key
- **game_id** - Reference to games table
- **user_id** - Reference to users table  
- **team_name** - 'Team A' or 'Team B'
- **assigned_position** - Player's assigned position
- **balance_score** - Algorithm confidence score (0-100)
- **algorithm_version** - Version tracking
- **created_at/updated_at** - Timestamps
- **Unique constraint** - One assignment per user per game

**Indexes:**
- game_id for fast game lookups
- team_name for team-based queries

---

## 🧠 **2. Core Algorithm Implementation**

### **Main Team Balancer (backend/app/algorithms/team_balancer.py)**
```python
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import random
from .balance_calculator import BalanceCalculator
from .position_optimizer import PositionOptimizer

@dataclass
class Player:
    id: int
    username: str
    first_name: str
    last_name: str
    skill_level: int
    preferred_position: str
    playing_style: str
    age_range: str
    position_preference: Optional[str] = None  # For this specific game

class TeamBalancer:
    """Smart team balancing algorithm for pickup football games"""
    
    def __init__(self):
        self.balance_calculator = BalanceCalculator()
        self.position_optimizer = PositionOptimizer()
        self.balance_weights = {
            'skill': 0.40,
            'position': 0.25,
            'style': 0.15,
            'age': 0.10,
            'fairness': 0.10  # Join order, etc.
        }
    
    def generate_balanced_teams(self, players: List[Player]) -> Dict:
        """
        Generate balanced teams from list of confirmed players
        
        Returns:
            {
                'team_a': List[Player],
                'team_b': List[Player], 
                'balance_score': float,
                'balance_details': Dict,
                'algorithm_version': str
            }
        """
        if len(players) < 4:
            raise ValueError("Need at least 4 players to create teams")
        
        # Step 1: Pre-process players
        processed_data = self._preprocess_players(players)
        
        # Step 2: Initial team creation using snake draft
        team_a, team_b = self._snake_draft_distribution(processed_data['sorted_players'])
        
        # Step 3: Optimize positions
        team_a, team_b = self.position_optimizer.optimize_positions(
            team_a, team_b, len(players)
        )
        
        # Step 4: Final balance optimization  
        team_a, team_b = self._optimize_final_balance(team_a, team_b)
        
        # Step 5: Calculate final balance score
        balance_score, balance_details = self.balance_calculator.calculate_total_balance(
            team_a, team_b
        )
        
        return {
            'team_a': team_a,
            'team_b': team_b,
            'balance_score': balance_score,
            'balance_details': balance_details,
            'algorithm_version': '1.0'
        }
    
    def _preprocess_players(self, players: List[Player]) -> Dict:
        """Organize players for optimal distribution"""
        # Sort by skill level (highest first for snake draft)
        sorted_players = sorted(players, key=lambda p: p.skill_level, reverse=True)
        
        # Group by positions
        by_position = {}
        for player in players:
            pos = player.position_preference or player.preferred_position
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append(player)
        
        # Calculate total skill
        total_skill = sum(p.skill_level for p in players)
        
        return {
            'sorted_players': sorted_players,
            'by_position': by_position,
            'total_skill': total_skill,
            'target_skill_per_team': total_skill / 2,
            'player_count': len(players)
        }
    
    def _snake_draft_distribution(self, sorted_players: List[Player]) -> Tuple[List[Player], List[Player]]:
        """Distribute players using snake draft method"""
        team_a = []
        team_b = []
        
        for i, player in enumerate(sorted_players):
            # Snake pattern: A, B, B, A, A, B, B, A, ...
            if i % 4 in [0, 3]:
                team_a.append(player)
            else:
                team_b.append(player)
        
        return team_a, team_b
    
    def _optimize_final_balance(self, team_a: List[Player], team_b: List[Player], max_swaps: int = 3) -> Tuple[List[Player], List[Player]]:
        """Final optimization through strategic swaps"""
        current_balance = self.balance_calculator.calculate_total_balance(team_a, team_b)[0]
        
        for _ in range(max_swaps):
            best_swap = None
            best_improvement = 0
            
            # Try all possible swaps
            for i, player_a in enumerate(team_a):
                for j, player_b in enumerate(team_b):
                    # Temporarily swap
                    team_a[i], team_b[j] = player_b, player_a
                    
                    # Calculate new balance
                    new_balance = self.balance_calculator.calculate_total_balance(team_a, team_b)[0]
                    improvement = new_balance - current_balance
                    
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_swap = (i, j)
                    
                    # Swap back
                    team_a[i], team_b[j] = player_a, player_b
            
            # Apply best swap if it improves balance
            if best_swap and best_improvement > 0.01:  # Minimum improvement threshold
                i, j = best_swap
                team_a[i], team_b[j] = team_b[j], team_a[i]
                current_balance += best_improvement
            else:
                break  # No more beneficial swaps
        
        return team_a, team_b
```

### **Balance Calculator (backend/app/algorithms/balance_calculator.py)**
```python
import math
from typing import List, Dict, Tuple
from .team_balancer import Player

class BalanceCalculator:
    """Calculate various balance metrics for teams"""
    
    def __init__(self):
        self.style_compatibility = {
            'Aggressive': {'complement': ['Technical', 'Balanced'], 'clash': ['Aggressive']},
            'Technical': {'complement': ['Physical', 'Creative'], 'clash': ['Defensive']},
            'Physical': {'complement': ['Technical', 'Creative'], 'clash': ['Physical']},
            'Balanced': {'complement': ['Aggressive', 'Technical'], 'clash': []},
            'Creative': {'complement': ['Physical', 'Defensive'], 'clash': []},
            'Defensive': {'complement': ['Creative', 'Aggressive'], 'clash': ['Technical']}
        }
    
    def calculate_total_balance(self, team_a: List[Player], team_b: List[Player]) -> Tuple[float, Dict]:
        """Calculate overall balance score and detailed breakdown"""
        
        skill_score = self.calculate_skill_balance(team_a, team_b)
        position_score = self.calculate_position_balance(team_a, team_b)
        style_score = self.calculate_style_balance(team_a, team_b)
        age_score = self.calculate_age_balance(team_a, team_b)
        size_score = self.calculate_size_balance(team_a, team_b)
        
        # Weighted total score
        total_score = (
            skill_score * 0.40 +
            position_score * 0.25 +
            style_score * 0.15 +
            age_score * 0.10 +
            size_score * 0.10
        ) * 100
        
        details = {
            'skill_balance': skill_score * 100,
            'position_balance': position_score * 100,
            'style_balance': style_score * 100,
            'age_balance': age_score * 100,
            'size_balance': size_score * 100,
            'team_a_avg_skill': sum(p.skill_level for p in team_a) / len(team_a),
            'team_b_avg_skill': sum(p.skill_level for p in team_b) / len(team_b),
            'skill_difference': abs(
                sum(p.skill_level for p in team_a) / len(team_a) - 
                sum(p.skill_level for p in team_b) / len(team_b)
            )
        }
        
        return total_score, details
    
    def calculate_skill_balance(self, team_a: List[Player], team_b: List[Player]) -> float:
        """Calculate skill balance between teams (0-1, higher is better)"""
        if not team_a or not team_b:
            return 0
        
        avg_a = sum(p.skill_level for p in team_a) / len(team_a)
        avg_b = sum(p.skill_level for p in team_b) / len(team_b)
        
        difference = abs(avg_a - avg_b)
        
        # Perfect balance = 1.0, decreases as difference increases
        # Max reasonable difference is 3 skill points
        return max(0, 1 - (difference / 3))
    
    def calculate_position_balance(self, team_a: List[Player], team_b: List[Player]) -> float:
        """Calculate positional balance between teams"""
        positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
        
        total_score = 0
        for position in positions:
            count_a = self._count_position(team_a, position)
            count_b = self._count_position(team_b, position)
            
            # Each team should have at least one of each position (except GK)
            min_required = 1 if position == 'Goalkeeper' else 1
            
            score_a = min(count_a / min_required, 1) if min_required > 0 else 1
            score_b = min(count_b / min_required, 1) if min_required > 0 else 1
            
            total_score += (score_a + score_b) / 2
        
        return total_score / len(positions)
    
    def calculate_style_balance(self, team_a: List[Player], team_b: List[Player]) -> float:
        """Calculate playing style balance and compatibility"""
        # Internal team style compatibility
        compat_a = self._calculate_team_style_compatibility(team_a)
        compat_b = self._calculate_team_style_compatibility(team_b)
        
        return (compat_a + compat_b) / 2
    
    def calculate_age_balance(self, team_a: List[Player], team_b: List[Player]) -> float:
        """Calculate age distribution balance"""
        age_ranges = ['18-25', '26-35', '36-45', '46+']
        
        dist_a = self._get_age_distribution(team_a, age_ranges)
        dist_b = self._get_age_distribution(team_b, age_ranges)
        
        # Calculate similarity between distributions
        similarity = 0
        for age_range in age_ranges:
            diff = abs(dist_a.get(age_range, 0) - dist_b.get(age_range, 0))
            similarity += 1 - diff
        
        return similarity / len(age_ranges)
    
    def calculate_size_balance(self, team_a: List[Player], team_b: List[Player]) -> float:
        """Ensure teams are equal size"""
        size_diff = abs(len(team_a) - len(team_b))
        return 1 - (size_diff / max(len(team_a), len(team_b), 1))
    
    def _count_position(self, team: List[Player], position: str) -> int:
        """Count players in a specific position"""
        return sum(1 for p in team if 
                  (p.position_preference or p.preferred_position) == position or
                  (p.position_preference or p.preferred_position) == 'Any')
    
    def _calculate_team_style_compatibility(self, team: List[Player]) -> float:
        """Calculate internal team style compatibility"""
        if len(team) < 2:
            return 1.0
        
        total_compatibility = 0
        pair_count = 0
        
        for i in range(len(team)):
            for j in range(i + 1, len(team)):
                style1 = team[i].playing_style
                style2 = team[j].playing_style
                
                if style1 in self.style_compatibility:
                    if style2 in self.style_compatibility[style1]['complement']:
                        total_compatibility += 1.0
                    elif style2 in self.style_compatibility[style1]['clash']:
                        total_compatibility += 0.0
                    else:
                        total_compatibility += 0.5
                else:
                    total_compatibility += 0.5
                
                pair_count += 1
        
        return total_compatibility / pair_count if pair_count > 0 else 1.0
    
    def _get_age_distribution(self, team: List[Player], age_ranges: List[str]) -> Dict[str, float]:
        """Get age distribution for a team"""
        if not team:
            return {}
        
        distribution = {}
        for age_range in age_ranges:
            count = sum(1 for p in team if p.age_range == age_range)
            distribution[age_range] = count / len(team)
        
        return distribution
```

---

## 🎯 **3. Backend API Implementation**

### **Add to main.py**
```python
# Add these imports at the top
from algorithms.team_balancer import TeamBalancer, Player
from algorithms.balance_calculator import BalanceCalculator

# Add these new endpoints after existing game endpoints

@app.post("/api/games/{game_id}/generate-teams")
async def generate_balanced_teams(
    game_id: int, 
    current_user: dict = Depends(verify_token)
):
    """Generate balanced teams for a game"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verify user is game creator
        cursor.execute("""
            SELECT created_by FROM games WHERE id = %s
        """, (game_id,))
        
        game = cursor.fetchone()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        if game[0] != current_user['id']:
            raise HTTPException(status_code=403, detail="Only game creator can generate teams")
        
        # Get confirmed players
        cursor.execute("""
            SELECT 
                gp.user_id, u.username, u.first_name, u.last_name,
                u.skill_level, u.preferred_position, u.playing_style, 
                u.age_range, gp.position_preference
            FROM game_participants gp
            JOIN users u ON gp.user_id = u.id
            WHERE gp.game_id = %s AND gp.status = 'confirmed'
            ORDER BY gp.joined_at
        """, (game_id,))
        
        participants = cursor.fetchall()
        
        if len(participants) < 4:
            raise HTTPException(status_code=400, detail="Need at least 4 confirmed players")
        
        # Convert to Player objects
        players = [
            Player(
                id=p[0], username=p[1], first_name=p[2], last_name=p[3],
                skill_level=p[4], preferred_position=p[5], playing_style=p[6],
                age_range=p[7], position_preference=p[8]
            )
            for p in participants
        ]
        
        # Generate balanced teams
        balancer = TeamBalancer()
        result = balancer.generate_balanced_teams(players)
        
        # Clear existing team assignments
        cursor.execute("""
            DELETE FROM team_assignments WHERE game_id = %s
        """, (game_id,))
        
        # Save team assignments
        for team_name, team_players in [('Team A', result['team_a']), ('Team B', result['team_b'])]:
            for player in team_players:
                cursor.execute("""
                    INSERT INTO team_assignments 
                    (game_id, user_id, team_name, assigned_position, balance_score, algorithm_version)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    game_id, player.id, team_name,
                    player.position_preference or player.preferred_position,
                    result['balance_score'], result['algorithm_version']
                ))
        
        conn.commit()
        
        # Return team assignments with player details
        return {
            "message": "Teams generated successfully",
            "balance_score": result['balance_score'],
            "balance_details": result['balance_details'],
            "teams": {
                "team_a": [
                    {
                        "id": p.id,
                        "username": p.username,
                        "name": f"{p.first_name} {p.last_name}",
                        "skill_level": p.skill_level,
                        "position": p.position_preference or p.preferred_position
                    }
                    for p in result['team_a']
                ],
                "team_b": [
                    {
                        "id": p.id,
                        "username": p.username,
                        "name": f"{p.first_name} {p.last_name}",
                        "skill_level": p.skill_level,
                        "position": p.position_preference or p.preferred_position
                    }
                    for p in result['team_b']
                ]
            }
        }
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate teams: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/games/{game_id}/teams")
async def get_game_teams(game_id: int):
    """Get current team assignments for a game"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                ta.team_name, ta.assigned_position, ta.balance_score,
                u.id, u.username, u.first_name, u.last_name, u.skill_level
            FROM team_assignments ta
            JOIN users u ON ta.user_id = u.id
            WHERE ta.game_id = %s
            ORDER BY ta.team_name, u.skill_level DESC
        """, (game_id,))
        
        assignments = cursor.fetchall()
        
        if not assignments:
            return {"teams": None, "message": "No teams generated yet"}
        
        # Organize by team
        teams = {"team_a": [], "team_b": []}
        balance_score = assignments[0][2] if assignments else 0
        
        for assignment in assignments:
            team_key = "team_a" if assignment[0] == "Team A" else "team_b"
            teams[team_key].append({
                "id": assignment[3],
                "username": assignment[4],
                "name": f"{assignment[5]} {assignment[6]}",
                "skill_level": assignment[7],
                "position": assignment[1]
            })
        
        return {
            "teams": teams,
            "balance_score": balance_score,
            "total_players": len(assignments)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")
    finally:
        cursor.close()
        conn.close()
```

---

## 🎨 **4. Frontend Implementation**

### **Team Generator Component (frontend/src/components/teams/TeamGenerator.js)**
```javascript
import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import BalanceScore from './BalanceScore';
import TeamDisplay from './TeamDisplay';
import './TeamGenerator.css';

const TeamGenerator = ({ game, onTeamsGenerated }) => {
  const { user } = useAuth();
  const [generating, setGenerating] = useState(false);
  const [teams, setTeams] = useState(null);
  const [balanceScore, setBalanceScore] = useState(null);
  const [error, setError] = useState('');

  const canGenerateTeams = () => {
    return game.created_by === user?.id && 
           game.confirmed_players >= 4 && 
           game.status === 'open';
  };

  const generateTeams = async () => {
    if (!canGenerateTeams()) return;

    setGenerating(true);
    setError('');

    try {
      const response = await fetch(`/api/games/${game.id}/generate-teams`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to generate teams');
      }

      const data = await response.json();
      
      setTeams(data.teams);
      setBalanceScore({
        score: data.balance_score,
        details: data.balance_details
      });

      if (onTeamsGenerated) {
        onTeamsGenerated(data);
      }

    } catch (error) {
      console.error('Error generating teams:', error);
      setError('Failed to generate teams. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const shuffleTeams = async () => {
    // Re-generate teams with slight randomization
    await generateTeams();
  };

  if (!canGenerateTeams()) {
    return (
      <div className="team-generator">
        <div className="generator-info">
          <h3>🤖 Smart Team Balancing</h3>
          <p>
            {game.confirmed_players < 4 
              ? `Need at least 4 players (currently ${game.confirmed_players})`
              : 'Only the game creator can generate balanced teams'
            }
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="team-generator">
      <div className="generator-header">
        <h3>🤖 Smart Team Balancing</h3>
        <p>Generate balanced teams based on skill levels and positions</p>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      <div className="generator-actions">
        <button 
          onClick={generateTeams}
          disabled={generating}
          className="generate-btn primary"
        >
          {generating ? '⏳ Generating...' : '🎯 Generate Balanced Teams'}
        </button>

        {teams && (
          <button 
            onClick={shuffleTeams}
            disabled={generating}
            className="shuffle-btn secondary"
          >
            🔄 Shuffle Teams
          </button>
        )}
      </div>

      {balanceScore && (
        <BalanceScore score={balanceScore} />
      )}

      {teams && (
        <TeamDisplay teams={teams} balanceScore={balanceScore} />
      )}
    </div>
  );
};

export default TeamGenerator;
```

### **Team Display Component (frontend/src/components/teams/TeamDisplay.js)**
```javascript
import React from 'react';

const TeamDisplay = ({ teams, balanceScore }) => {
  const getSkillColor = (skillLevel) => {
    if (skillLevel >= 8) return '#4CAF50'; // Green
    if (skillLevel >= 6) return '#FF9800'; // Orange  
    if (skillLevel >= 4) return '#2196F3'; // Blue
    return '#9E9E9E'; // Gray
  };

  const getPositionIcon = (position) => {
    const icons = {
      'Goalkeeper': '🥅',
      'Defender': '🛡️',
      'Midfielder': '⚽',
      'Forward': '🥅',
      'Any': '🔄'
    };
    return icons[position] || '⚽';
  };

  const calculateTeamAverage = (team) => {
    const total = team.reduce((sum, player) => sum + player.skill_level, 0);
    return (total / team.length).toFixed(1);
  };

  return (
    <div className="team-display">
      <div className="teams-container">
        {/* Team A */}
        <div className="team-section team-a">
          <div className="team-header">
            <h4>⚡ Team A</h4>
            <div className="team-stats">
              <span className="avg-skill">
                Avg: {calculateTeamAverage(teams.team_a)}/10
              </span>
              <span className="player-count">
                {teams.team_a.length} players
              </span>
            </div>
          </div>
          
          <div className="team-players">
            {teams.team_a.map((player) => (
              <div key={player.id} className="player-card">
                <div className="player-info">
                  <span className="player-name">{player.name}</span>
                  <span className="player-username">@{player.username}</span>
                </div>
                <div className="player-stats">
                  <span 
                    className="skill-badge"
                    style={{ backgroundColor: getSkillColor(player.skill_level) }}
                  >
                    {player.skill_level}
                  </span>
                  <span className="position-badge">
                    {getPositionIcon(player.position)} {player.position}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* VS Divider */}
        <div className="vs-divider">
          <span>VS</span>
        </div>

        {/* Team B */}
        <div className="team-section team-b">
          <div className="team-header">
            <h4>🔥 Team B</h4>
            <div className="team-stats">
              <span className="avg-skill">
                Avg: {calculateTeamAverage(teams.team_b)}/10
              </span>
              <span className="player-count">
                {teams.team_b.length} players
              </span>
            </div>
          </div>
          
          <div className="team-players">
            {teams.team_b.map((player) => (
              <div key={player.id} className="player-card">
                <div className="player-info">
                  <span className="player-name">{player.name}</span>
                  <span className="player-username">@{player.username}</span>
                </div>
                <div className="player-stats">
                  <span 
                    className="skill-badge"
                    style={{ backgroundColor: getSkillColor(player.skill_level) }}
                  >
                    {player.skill_level}
                  </span>
                  <span className="position-badge">
                    {getPositionIcon(player.position)} {player.position}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeamDisplay;
```

### **Balance Score Component (frontend/src/components/teams/BalanceScore.js)**
```javascript
import React from 'react';

const BalanceScore = ({ score }) => {
  const getScoreColor = (value) => {
    if (value >= 85) return '#4CAF50'; // Green - Excellent
    if (value >= 70) return '#FF9800'; // Orange - Good  
    if (value >= 50) return '#2196F3'; // Blue - Fair
    return '#f44336'; // Red - Poor
  };

  const getScoreLabel = (value) => {
    if (value >= 85) return 'Excellent Balance';
    if (value >= 70) return 'Good Balance';
    if (value >= 50) return 'Fair Balance';
    return 'Needs Improvement';
  };

  return (
    <div className="balance-score">
      <div className="score-header">
        <h4>⚖️ Team Balance Score</h4>
        <div 
          className="score-value"
          style={{ color: getScoreColor(score.score) }}
        >
          {Math.round(score.score)}/100
        </div>
      </div>
      
      <div className="score-label">
        {getScoreLabel(score.score)}
      </div>

      <div className="score-breakdown">
        <div className="breakdown-item">
          <span className="breakdown-label">Skill Balance:</span>
          <div className="breakdown-bar">
            <div 
              className="breakdown-fill"
              style={{ 
                width: `${score.details.skill_balance}%`,
                backgroundColor: getScoreColor(score.details.skill_balance)
              }}
            />
          </div>
          <span className="breakdown-value">
            {Math.round(score.details.skill_balance)}%
          </span>
        </div>

        <div className="breakdown-item">
          <span className="breakdown-label">Position Balance:</span>
          <div className="breakdown-bar">
            <div 
              className="breakdown-fill"
              style={{ 
                width: `${score.details.position_balance}%`,
                backgroundColor: getScoreColor(score.details.position_balance)
              }}
            />
          </div>
          <span className="breakdown-value">
            {Math.round(score.details.position_balance)}%
          </span>
        </div>

        <div className="breakdown-item">
          <span className="breakdown-label">Style Balance:</span>
          <div className="breakdown-bar">
            <div 
              className="breakdown-fill"
              style={{ 
                width: `${score.details.style_balance}%`,
                backgroundColor: getScoreColor(score.details.style_balance)
              }}
            />
          </div>
          <span className="breakdown-value">
            {Math.round(score.details.style_balance)}%
          </span>
        </div>
      </div>

      <div className="skill-difference">
        <small>
          Skill difference: {score.details.skill_difference.toFixed(1)} points
        </small>
      </div>
    </div>
  );
};

export default BalanceScore;
```

---

## 🎨 **5. CSS Styling (frontend/src/components/teams/TeamGenerator.css)**

```css
.team-generator {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin: 20px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.generator-header h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 1.3rem;
}

.generator-header p {
  margin: 0 0 20px 0;
  color: #666;
  font-size: 0.95rem;
}

.generator-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.generate-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.shuffle-btn {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.shuffle-btn:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
  border-left: 4px solid #c62828;
}

/* Balance Score Styles */
.balance-score {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid #e9ecef;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.score-header h4 {
  margin: 0;
  color: #333;
}

.score-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.score-label {
  text-align: center;
  font-weight: 600;
  margin-bottom: 16px;
  color: #555;
}

.score-breakdown {
  display: grid;
  gap: 12px;
}

.breakdown-item {
  display: grid;
  grid-template-columns: 120px 1fr 50px;
  gap: 12px;
  align-items: center;
  font-size: 0.9rem;
}

.breakdown-label {
  color: #666;
  font-weight: 500;
}

.breakdown-bar {
  background: #e0e0e0;
  border-radius: 10px;
  height: 8px;
  overflow: hidden;
}

.breakdown-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.breakdown-value {
  text-align: right;
  font-weight: 600;
  color: #333;
}

.skill-difference {
  text-align: center;
  margin-top: 12px;
  color: #666;
}

/* Team Display Styles */
.team-display {
  margin-top: 20px;
}

.teams-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 20px;
  align-items: start;
}

.team-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  border: 2px solid transparent;
}

.team-a {
  border-color: #667eea;
}

.team-b {
  border-color: #764ba2;
}

.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e9ecef;
}

.team-header h4 {
  margin: 0;
  font-size: 1.2rem;
}

.team-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.avg-skill {
  font-weight: 600;
  color: #333;
}

.player-count {
  font-size: 0.85rem;
  color: #666;
}

.vs-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  font-weight: bold;
  font-size: 1.1rem;
  margin-top: 60px;
}

.team-players {
  display: grid;
  gap: 12px;
}

.player-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.player-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.player-name {
  font-weight: 600;
  color: #333;
}

.player-username {
  font-size: 0.85rem;
  color: #666;
}

.player-stats {
  display: flex;
  gap: 8px;
  align-items: center;
}

.skill-badge {
  background: #4CAF50;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

.position-badge {
  background: #e9ecef;
  color: #495057;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .teams-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .vs-divider {
    margin-top: 0;
    order: -1;
    margin-bottom: 16px;
  }
  
  .generator-actions {
    flex-direction: column;
  }
  
  .breakdown-item {
    grid-template-columns: 100px 1fr 40px;
    gap: 8px;
  }
  
  .player-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .player-stats {
    align-self: flex-end;
  }
}
```

---

## 🚀 **6. Integration Steps**

### **Step 1: Database Setup**
```bash
# Run the new database migration
psql -U postgres -d pickup_football -f database/05_create_team_assignments_table.sql
```

### **Step 2: Backend Integration**
```python
# Add to backend/app/main.py
# Copy the new endpoints from section 3 above
```

### **Step 3: Frontend Integration**
```javascript
// Add to your GameCard component or Dashboard
import TeamGenerator from '../teams/TeamGenerator';

// Inside your game display component:
{game.created_by === user?.id && game.confirmed_players >= 4 && (
  <TeamGenerator 
    game={game} 
    onTeamsGenerated={(data) => {
      console.log('Teams generated:', data);
      // Handle the generated teams
    }}
  />
)}
```

---

## 🧪 **7. Testing the Implementation**

### **Test the Algorithm**
```python
# Create test file: backend/test_team_balancer.py
from algorithms.team_balancer import TeamBalancer, Player

def test_basic_balancing():
    players = [
        Player(1, "player1", "John", "Doe", 8, "Forward", "Aggressive", "25-35"),
        Player(2, "player2", "Jane", "Smith", 6, "Midfielder", "Technical", "18-25"),
        Player(3, "player3", "Bob", "Wilson", 7, "Defender", "Physical", "26-35"),
        Player(4, "player4", "Alice", "Brown", 5, "Goalkeeper", "Balanced", "18-25"),
        Player(5, "player5", "Charlie", "Davis", 8, "Forward", "Creative", "36-45"),
        Player(6, "player6", "Diana", "Miller", 6, "Midfielder", "Defensive", "26-35"),
    ]
    
    balancer = TeamBalancer()
    result = balancer.generate_balanced_teams(players)
    
    print(f"Balance Score: {result['balance_score']:.1f}/100")
    print(f"Team A: {len(result['team_a'])} players")
    print(f"Team B: {len(result['team_b'])} players")
    
    # Check skill balance
    avg_a = sum(p.skill_level for p in result['team_a']) / len(result['team_a'])
    avg_b = sum(p.skill_level for p in result['team_b']) / len(result['team_b'])
    print(f"Skill difference: {abs(avg_a - avg_b):.1f}")

if __name__ == "__main__":
    test_basic_balancing()
```

### **Test the API**
```bash
# Test team generation endpoint
curl -X POST http://localhost:8000/api/games/1/generate-teams \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# Test get teams endpoint  
curl http://localhost:8000/api/games/1/teams
```

---

## 📈 **8. Deployment Checklist**

- [ ] Database migration completed
- [ ] Algorithm files added to backend
- [ ] API endpoints tested
- [ ] Frontend components integrated
- [ ] CSS styling applied
- [ ] Error handling implemented
- [ ] Mobile responsiveness verified
- [ ] Performance testing completed
- [ ] User permission checks working

---

**This implementation guide provides everything needed to add smart team balancing to your pickup football app. The algorithm is designed to be robust, extensible, and user-friendly while maintaining the mobile-first approach of your application.**
