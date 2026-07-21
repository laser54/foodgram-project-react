import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders the sign-in page for an anonymous visitor', async () => {
  render(
    <MemoryRouter initialEntries={['/signin']}>
      <App />
    </MemoryRouter>
  );

  expect(await screen.findByRole('heading', { name: /Войти на сайт/i }))
    .toBeInTheDocument();
});
