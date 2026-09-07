import { Route, Routes } from 'react-router-dom'
import Layout from './components/layout/Layout'
import RequireAuth from './features/auth/RequireAuth'
import About from './routes/About'
import Chat from './routes/Chat'
import Login from './routes/Login'
import Register from './routes/Register'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route element={<RequireAuth />}>
          <Route index element={<Chat />} />
        </Route>
        <Route path="about" element={<About />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Route>
    </Routes>
  )
}

export default App
