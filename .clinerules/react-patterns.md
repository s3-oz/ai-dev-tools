---
description: Best practices and patterns for React development across all projects
author: AI-Dev-Tools
version: 1.0
tags: ["react", "frontend", "components", "hooks", "patterns"]
globs: ["**/*.jsx", "**/*.tsx", "**/*.js", "**/*.ts"]
---

# React Best Practices and Patterns

## Purpose

This rule defines consistent patterns and best practices for React development across all projects. Following these guidelines ensures maintainable, performant, and accessible React applications with a consistent architecture and component design.

## Guidelines

### Core Principles

- **Component-Based Architecture**: Break UI into small, reusable components with clear responsibilities
- **Unidirectional Data Flow**: Data flows down from parent to child components
- **Declarative Programming**: Describe what the UI should look like, not how to change it
- **Composition Over Inheritance**: Use component composition instead of inheritance to reuse code
- **Single Responsibility**: Each component should do one thing well

### Specific Rules

#### Component Structure

- **Functional Components**: Use functional components with hooks instead of class components
  ```jsx
  // Preferred
  function UserProfile({ user }) {
    return <div>{user.name}</div>;
  }
  
  // Avoid
  class UserProfile extends React.Component {
    render() {
      return <div>{this.props.user.name}</div>;
    }
  }
  ```

- **Component Organization**:
  - One component per file (except for small, related components)
  - Name files the same as the component (e.g., `Button.jsx` for `Button` component)
  - Group related components in folders
  - Create an index.js file to export components from folders

- **Component Naming**:
  - Use PascalCase for component names (e.g., `UserProfile`)
  - Use descriptive names that reflect the component's purpose
  - Prefix higher-order components with "with" (e.g., `withAuth`)
  - Suffix custom hooks with "use" (e.g., `useFormValidation`)

#### Props

- **Props Naming**:
  - Use camelCase for prop names
  - Use boolean props without values for flags (e.g., `<Button primary />`)
  - Prefix boolean props with "is", "has", or "should" (e.g., `isActive`, `hasError`)

- **Props Handling**:
  - Destructure props in function parameters
  - Provide default values for optional props
  - Use prop-types or TypeScript for type checking
  - Keep required props to a minimum

```jsx
// Good
function Button({ primary, disabled, children, onClick }) {
  return (
    <button 
      className={primary ? 'btn-primary' : 'btn-secondary'}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

Button.defaultProps = {
  primary: false,
  disabled: false,
  onClick: () => {},
};
```

#### State Management

- **Local State**:
  - Use `useState` for simple component state
  - Use `useReducer` for complex state logic
  - Keep state as local as possible to the components that need it

- **Global State**:
  - Use Context API for state that needs to be accessed by many components
  - Consider Redux, Zustand, or other state management libraries for complex applications
  - Organize global state by domain/feature

- **State Updates**:
  - Treat state as immutable
  - Use functional updates for state that depends on previous state
  - Batch related state updates

```jsx
// Good - Functional update
setCount(prevCount => prevCount + 1);

// Good - Immutable update
setUser(prevUser => ({ ...prevUser, name: 'New Name' }));
```

#### Hooks

- **Built-in Hooks**:
  - Use `useEffect` for side effects
  - Use `useMemo` for expensive calculations
  - Use `useCallback` for functions passed to child components
  - Use `useRef` for mutable values that don't trigger re-renders

- **Custom Hooks**:
  - Extract reusable logic into custom hooks
  - Name custom hooks with "use" prefix
  - Keep custom hooks focused on a single concern
  - Document custom hooks with JSDoc comments

```jsx
// Good - Custom hook
function useWindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 });
  
  useEffect(() => {
    function updateSize() {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    }
    
    window.addEventListener('resize', updateSize);
    updateSize();
    
    return () => window.removeEventListener('resize', updateSize);
  }, []);
  
  return size;
}
```

#### Performance Optimization

- **Memoization**:
  - Use `React.memo` for components that render often with the same props
  - Use `useMemo` for expensive calculations
  - Use `useCallback` for event handlers passed to optimized child components

- **Rendering**:
  - Avoid unnecessary re-renders
  - Keep component trees shallow
  - Use virtualization for long lists (react-window or react-virtualized)
  - Use code-splitting with `React.lazy` and `Suspense`

- **Dependencies**:
  - Specify all dependencies in useEffect, useMemo, and useCallback dependency arrays
  - Keep dependency arrays as small as possible

#### Styling

- **CSS-in-JS**:
  - Prefer styled-components or emotion for component-specific styling
  - Use theme providers for consistent design
  - Avoid inline styles except for dynamic values

- **CSS Modules**:
  - Alternative to CSS-in-JS
  - Scope styles to components
  - Use consistent naming conventions

- **Global Styles**:
  - Use global styles for typography, colors, and other design tokens
  - Define a consistent theme

## Examples

### Good Component Example

```jsx
// UserProfile.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Avatar } from './Avatar';
import { UserStats } from './UserStats';
import { useUserData } from '../hooks/useUserData';
import './UserProfile.css';

function UserProfile({ userId, isEditable }) {
  const { user, loading, error } = useUserData(userId);
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading user</div>;
  if (!user) return null;
  
  return (
    <div className="user-profile">
      <Avatar src={user.avatarUrl} size="large" />
      <h2>{user.name}</h2>
      <button onClick={() => setIsExpanded(!isExpanded)}>
        {isExpanded ? 'Show Less' : 'Show More'}
      </button>
      
      {isExpanded && (
        <>
          <p>{user.bio}</p>
          <UserStats stats={user.stats} />
        </>
      )}
      
      {isEditable && (
        <button onClick={() => /* handle edit */}>
          Edit Profile
        </button>
      )}
    </div>
  );
}

UserProfile.propTypes = {
  userId: PropTypes.string.isRequired,
  isEditable: PropTypes.bool,
};

UserProfile.defaultProps = {
  isEditable: false,
};

export default UserProfile;
```

### Bad Component Example

```jsx
// Bad example
class Profile extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userData: null,
      expanded: false,
    };
  }
  
  componentDidMount() {
    // Directly fetch in component
    fetch(`/api/users/${this.props.id}`)
      .then(res => res.json())
      .then(data => this.setState({ userData: data }));
  }
  
  render() {
    if (!this.state.userData) return <div>Loading...</div>;
    
    return (
      <div>
        <img src={this.state.userData.avatar} style={{ width: 50, height: 50 }} />
        <h2>{this.state.userData.name}</h2>
        <button onClick={() => this.setState({ expanded: !this.state.expanded })}>
          Toggle
        </button>
        
        {this.state.expanded ? (
          <div>
            <p>{this.state.userData.bio}</p>
            <div>
              <span>Followers: {this.state.userData.followers}</span>
              <span>Following: {this.state.userData.following}</span>
            </div>
          </div>
        ) : null}
        
        {this.props.editable && <button>Edit</button>}
      </div>
    );
  }
}
```

## Special Cases and Exceptions

- **Legacy Projects**: When working with existing class-based components, follow the established patterns for consistency.
- **Performance-Critical Components**: In rare cases, you might need to use more imperative approaches for performance-critical components.
- **External Libraries**: When integrating with external libraries that use different patterns, create wrapper components that follow these guidelines.

## Related Rules

- [Coding Standards](./coding-standards.md): General coding standards that apply to all code, including React
- Accessibility Guidelines: Guidelines for creating accessible React components

## References

- [React Official Documentation](https://reactjs.org/docs/getting-started.html)
- [React Hooks Documentation](https://reactjs.org/docs/hooks-intro.html)
- [Airbnb React/JSX Style Guide](https://github.com/airbnb/javascript/tree/master/react)

## Changelog

- v1.0 (2025-05-18): Initial version
