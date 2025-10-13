export interface AppNavigationItem {
    id: string;
    label: string;
    path: string;
    description: string;
}

export interface AppTheme {
    colors: Record<string, string>;
    radius: Record<string, string>;
    fontFamily: Record<string, string | string[]>;
}

export interface AppInitializationResult {
    container: unknown;
    router: unknown;
    queryClient: unknown;
    theme: AppTheme;
    rootTree: unknown;
}

export interface AppRouterOptions {
    theme?: AppTheme | null;
    navigation?: AppNavigationItem[];
    basename?: string;
    initialEntries?: string[];
}

export interface InitializeAppOptions extends AppRouterOptions {
    container?: unknown;
    router?: unknown;
    queryClient?: unknown;
    appOptions?: Record<string, unknown>;
}

export declare const appNavigation: AppNavigationItem[];

export declare function initializeApp(options?: InitializeAppOptions): AppInitializationResult;

export declare function createAppRouter(options?: AppRouterOptions): unknown;

export declare function createRouteConfig(options?: AppRouterOptions): unknown[];

export declare function summarizeRoutes(routes?: unknown[]): Array<{ id: string; path: string | null; hasChildren: boolean }>;

export declare function createAppQueryClient(overrides?: Record<string, unknown>): unknown;

export declare function primeQueryClient(client: any, entries?: Array<{ key: unknown; value: unknown }>): any;

export declare const queryKeys: Record<string, unknown>;

export declare function createAppTheme(overrides?: Partial<AppTheme>): AppTheme;

export declare const appThemeTokens: AppTheme;

export declare function createThemeTokensSummary(theme?: AppTheme): {
    paletteSize: number;
    radiusScale: string[];
    fonts: Record<string, string>;
};
