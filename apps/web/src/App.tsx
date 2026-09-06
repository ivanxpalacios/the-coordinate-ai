import { Route, Routes } from 'react-router-dom'
import Layout from './components/layout/Layout'
import About from './routes/About'
import Chat from './routes/Chat'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Chat />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  )
}

export default App
