//package tdtu.edu.security;
//
//import org.springframework.cloud.mvc.gateway.filter.GatewayFilterChain;
//import org.springframework.cloud.gateway.server.mvc.filter.*;
//import org.springframework.cloud.gateway.filter.GlobalFilter;
//import org.springframework.context.annotation.Bean;
//import org.springframework.core.Ordered;
//import org.springframework.http.HttpStatus;
//import org.springframework.web.server.ServerWebExchange;
//import reactor.core.publisher.Mono;
//
//import java.util.concurrent.atomic.AtomicBoolean;
//
//public class SingleRequestFilter implements GlobalFilter, Ordered {
//
//    @Bean
//    public GlobalFilter customFilter() {
//        return new CustomGlobalFilter();
//    }
//
//    public class CustomGlobalFilter implements GlobalFilter, Ordered {
//
//        @Override
//        public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
//            log.info("custom global filter");
//            return chain.filter(exchange);
//        }
//
//        @Override
//        public int getOrder() {
//            return -1;
//        }
//    }
//}