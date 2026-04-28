# 🎨 Theme Engine — Motor de Temas Visuais

## Como funciona

O frontend Next.js carrega variáveis CSS diretamente do banco via API:

```typescript
// Exemplo de ThemeConfig armazenado no banco
const theme = {
  '--color-primary': '#2E7D32',
  '--color-secondary': '#81C784',
  '--color-accent': '#FF8F00',
  '--color-bg': '#FAFAFA',
  '--font-display': 'Cabinet Grotesk',
  '--font-body': 'Satoshi',
  '--radius-md': '0.75rem',
  '--sidebar-style': 'dark',
  '--logo-url': '/tenants/pet-shop-xyz/logo.svg'
};

// Aplicado no <html> via data-theme do tenant
Object.entries(theme).forEach(([key, value]) => {
  document.documentElement.style.setProperty(key, value);
});
```

## Perfis de Tema por Nicho

| Nicho | Paleta | Estilo |
|---|---|---|
| Pet Shop | Verde + laranja quente | Amigável, arredondado |
| Oficina / Mecânica | Azul escuro + laranja | Industrial, sólido |
| Barbearia | Preto + dourado + creme | Premium, masculino |
| Produção / Fábrica | Cinza industrial + verde | Técnico, preciso |
| Salão de Beleza | Rosa + roxo suave | Elegante, moderno |
| Clínica | Branco + azul claro | Limpo, confiável |
| Varejo | Laranja + azul vibrante | Energético, comercial |

## Geração Automática pela IA

O AI Engine gera o ThemeConfig inicial baseado no nicho. O tenant pode customizar depois via painel de branding, mas a IA já entrega um ponto de partida profissional e coerente sem necessidade de um designer.
