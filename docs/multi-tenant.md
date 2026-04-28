# 🏢 Multi-Tenant — Isolamento por Empresa

## Estratégia

Usamos **Row-Level Isolation** (isolamento por linha no banco) com `tenant_id` em todas as tabelas operacionais. Cada empresa tem seus próprios dados completamente isolados, mas compartilham a mesma infraestrutura.

## Subdomínio por Tenant

Cada empresa recebe um subdomínio automático:
- `petshop-xyz.nexuscore.app`
- `oficina-silva.nexuscore.app`
- Domínio próprio via CNAME (planos premium)

## Middleware de Tenant

```typescript
// NestJS Middleware — injeta tenant_id em toda request
@Injectable()
export class TenantMiddleware implements NestMiddleware {
  async use(req: Request, res: Response, next: NextFunction) {
    const hostname = req.hostname; // ex: petshop-xyz.nexuscore.app
    const slug = hostname.split('.')[0];
    const tenant = await this.tenantService.findBySlug(slug);
    if (!tenant) throw new NotFoundException('Tenant not found');
    req['tenant'] = tenant;
    next();
  }
}
```

## Planos e Limites

| Plano | Usuários | Módulos | IA Calls/mês | Preço |
|---|---|---|---|---|
| Starter | 2 | 4 módulos | 10 | R$ 79/mês |
| Growth | 10 | 7 módulos | 50 | R$ 197/mês |
| Pro | Ilimitado | Todos | 200 | R$ 397/mês |
| Enterprise | Ilimitado | Todos + white-label | Ilimitado | Negociado |
